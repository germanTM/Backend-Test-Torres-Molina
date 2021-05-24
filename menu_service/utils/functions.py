from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from django.core.files import File
from datetime import *
from ..models import Files, Menu_Meal_Options, Menu, Daily_Menu, Meal_Options_Dishes
import os, shutil

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def empty_daily_menu_data():
    Files.objects.all().delete()
    folder = settings.BASE_DIR+'/pdf2'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
def menu_details(request, menu_id = 0):
    optionsOfMenu = 0
    weekDay = date.today().weekday()
    today = date.today().strftime("%Y-%m-%d")
    if menu_id:
        optionsOfMenu = Menu_Meal_Options.objects.prefetch_related('menu').filter(menu_id=menu_id)
    else:
        todaysMenu = Menu.objects.filter(scheduled_date=today).first()
        todaysMenuId = todaysMenu.id
        if todaysMenuId:
            optionsOfMenu = Menu_Meal_Options.objects.prefetch_related('menu').filter(menu_id=todaysMenuId)
        else:  
            weekDay = Daily_Menu.objects.filter(id=weekDay+1).first()
            menuOfTheDay = weekDay.menu_id
            if menuOfTheDay:
                optionsOfMenu = Menu_Meal_Options.objects.prefetch_related('menu').filter(menu_id=menuOfTheDay)
            else:
                messages.info(request, "There's no menu for today")
    if optionsOfMenu:
        optionData = []
        optionDishRelation = []
        for option in optionsOfMenu:
            optionData = []
            dishesInOption = Meal_Options_Dishes.objects.prefetch_related('dish').filter(meal_option_id=option.meal_option_id)
            optionData.append(str(option.meal_option))
            for dish in dishesInOption:
                optionData.append(str(dish.dish))
            optionDishRelation.append({option.meal_option_id:optionData})
        return optionDishRelation
    return None