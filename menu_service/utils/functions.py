from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from django.core.files import File
from datetime import *
import pytz
from ..models import Dish_Ingredient, Files, Menu_Meal_Options, Menu, Daily_Menu, Meal_Options_Dishes
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
    optionDishRelation = []
    try:
        if menu_id:
            optionsOfMenu = Menu_Meal_Options.objects.select_related('meal_option')
        else:
            todaysMenu = Menu.objects.filter(scheduled_date=today).first()
            todaysMenuId = todaysMenu.id
            if todaysMenuId:
                optionsOfMenu = Menu_Meal_Options.objects.select_related('meal_option')
            else:  
                weekDay = Daily_Menu.objects.filter(id=weekDay+1).first()
                menuOfTheDay = weekDay.menu_id
                if menuOfTheDay:
                    optionsOfMenu = Menu_Meal_Options.objects.select_related('meal_option')
                else:
                    return {'error': 1, 'message': "There's no menu for today", "optionDishRelation":''}
        if optionsOfMenu:
            dishOptionRelation = Meal_Options_Dishes.objects.select_related('meal_option')
            dishesIngredients = Dish_Ingredient.objects.select_related('dish')
            return {'error': 0, 'message': '', 'optionDishRelation': optionsOfMenu, 'dishesIngredients': dishesIngredients, 'dishOptionRelation':dishOptionRelation}
    except Exception as e:
        return {'error': 1, 'message': str(e), 'optionDishRelation': ''}
    return {'error': 0, 'message': '', 'optionDishRelation': optionDishRelation}

def get_timezone_time(timezone):
    timeToEvalueate = pytz.timezone(timezone)
    chileCurrentHour = datetime.now(timeToEvalueate)
    return chileCurrentHour

def get_limit_hour_for_order(timezone):
    startLimitHour = '11'
    startLimitMinute = '00'
    limitHour = int(startLimitHour)*60 + int(startLimitMinute)
    currentTime = get_timezone_time(timezone).hour*60 + get_timezone_time(timezone).minute
    onTime = True if limitHour > currentTime else False
    return onTime