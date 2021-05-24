from celery.decorators import task
from celery.utils.log import get_task_logger
from  .models import Files, Menu, Meal_Options_Dishes, Menu_Meal_Options, Daily_Menu
from django.conf import settings
from slack_sdk import WebClient
from django.contrib import messages
from django.shortcuts import redirect
from datetime import *
from .utils import functions
from django.core.files import File
from io import BytesIO
from django.http import HttpResponse
import os

logger = get_task_logger(__name__)

@task(name="send_menu_through_slack")
def send_menu_by_slack_task():
    optionsOfMenu = 0
    weekDay = date.today().weekday()
    today = date.today().strftime("%Y-%m-%d")
    print(today)
    todaysMenu = Menu.objects.filter(scheduled_date=today).first()
    todaysMenuId = todaysMenu.id if todaysMenu else 0
    if todaysMenuId:
        optionsOfMenu = Menu_Meal_Options.objects.prefetch_related('menu').filter(menu_id=todaysMenuId)
    else:  
        dailyMenu = Daily_Menu.objects.filter(id=weekDay+1).first()
        menuOfTheDay = dailyMenu.menu_id if dailyMenu else 0
        if menuOfTheDay:
            optionsOfMenu = Menu_Meal_Options.objects.prefetch_related('menu').filter(menu_id=menuOfTheDay)
        else:
            messages.info("There's no menu for today")
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
        context = {'data':optionDishRelation}
        pdf = functions.render_to_pdf('pdf/daily-menu.html', context)
        functions.empty_daily_menu_data()
        savedFile = Files()
        savedFile.name.save('Menu', File(BytesIO(pdf.content)))
        client = WebClient(token=settings.SLACK_API_TOKEN)
        client.chat_postMessage(channel='#chile', text = "Excelente tarde! es el menú del día: "+os.path.join('http://localhost:8000/generatePDF',settings.MENU_URL))
        return HttpResponse(pdf, content_type='application/pdf')
    
    return redirect('home')