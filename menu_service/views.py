from django.shortcuts import render, redirect
from  .models import Order, Ordered_Dishes, Meal_Option, Meal_Options_Dishes, Menu, Ordered_Dishes_Ingredients_Details
from django.contrib import messages
from .decorators.decorators import admin_permissions, autheticated_user, autheticated_user
from datetime import *
from django.http import HttpResponse
from django.conf import settings
from . import tasks

# Create your views here.
from .forms import CustomizeIngredientsForm, CreateIngredientForm, CreateDishForm, CreateMealOptionForm, CreateMenuForm
from .utils import functions

@autheticated_user
@admin_permissions
def create_ingredient(request):
    form = CreateIngredientForm()
    context = {"form":form}
    if request.method=='POST':
        form = CreateIngredientForm(request.POST)
        if form.is_valid():
            ingredientCreation = CreateIngredientForm.save(request)
            if ingredientCreation.get('error') == 1:
                return render(request, "create-ingredient.html", context, status=400)
            else:
                messages.info(request, "Ingredient created succesfully")
                return render(request, "create-ingredient.html", context, status=201)
    return render(request, "create-ingredient.html", context, status=302)

@autheticated_user
@admin_permissions
def create_dish(request):
    form = CreateDishForm()
    context = {'form':form}
    if request.method == 'POST':
        form = CreateDishForm(request.POST)
        if form.is_valid():
            savedDish = CreateDishForm.save(request)
            if savedDish.get('error') == 1:
                messages.info(request, "Error at creating dish, motive:" +savedDish.get('message'))
                return render(request, "create-dish.html", context, status=400)
            else:
                messages.info(request, "Dish created succesfully")
                return render(request, "create-dish.html", context, status=201)
        else:
            messages.info(request, "Create dish form is incorrect")
            return render(request, "create-dish.html", context, status=400)
    return render(request, "create-dish.html", context)

@autheticated_user
@admin_permissions
def create_meal_option(request):
    form = CreateMealOptionForm()
    if request.method == 'POST':
        form = CreateMealOptionForm(request.POST)
        if form.is_valid():
            dishes = dict(request.POST)['dishes']
            optionName = request.POST.get('name')
            existingOption = Meal_Option.objects.filter(name=optionName)
            if existingOption:
                messages.info(request, "Option is already registered in the data")
            else:
                savedOption = Meal_Option.objects.create(name=optionName)
                optionId = savedOption.id
                for item in dishes:
                    dishOption = Meal_Options_Dishes(dish_id = item, meal_option_id = optionId)
                    dishOption.save()
    context = {'form':form}
    return render(request, "create-meal-option.html", context)

@autheticated_user
@admin_permissions
def create_menu(request, menu_id = 0):
    form = CreateMenuForm()
    context = {'form':form}
    if request.method == 'POST':
        form = CreateMenuForm(request.POST)
        if form.is_valid():
            savedMenu = CreateMenuForm.save(request, menu_id)
            if savedMenu.get('error') == 1:
                print(savedMenu.get('message'))
                messages.info(request, "Error at creating menu, motive:" +savedMenu.get('message'))
                return render(request, "create-menu.html", context, status=400)
            else:
                messages.info(request, "Dish created succesfully")
                return render(request, "create-menu.html", context, status=201)
        else:
            messages.info(request, "Create menu form is incorrect")
            return render(request, "create-menu.html", context, status=400)
    return render(request, "create-menu.html", context)

@autheticated_user
@admin_permissions
def list_menu(request):
    listMenu = Menu.objects.all()
    context = {'menus':listMenu}
    return render(request, 'list-menus.html', context)

@autheticated_user
@admin_permissions
def menu_details(request, menu_id = 0):
    menuDetails = functions.menu_details(request, menu_id)
    if menuDetails:
        context = {'data': menuDetails}
        return render(request, 'list-menu-options.html', context)
    messages.info(request, "There's no menu for today")
    return redirect('home')

@autheticated_user
def show_menu_for_order(request):
    menuDetails = functions.menu_details(request)
    if menuDetails:
        context = {'data': menuDetails}
        return render(request, 'list-menu-of-the-day.html', context)
    messages.info(request, "There's no menu for today")
    return redirect('home')

@autheticated_user
def view_ingredients(request, option):
    form = CustomizeIngredientsForm(option)
    if request.method == 'POST':
        formRequest = request.POST
        form.save(formRequest, option, request)
    context={"form": form}
    return render(request, 'customize-ingredients.html', context)

def view_orders(request):
    resultData=[]
    today = date.today().strftime("%Y-%m-%d")
    context = {}
    dishIngredients = []
    dishData = []
    username=''
    ordersDetails = Ordered_Dishes.objects.all()
    for detail in ordersDetails:
        dishIngredients = []
        if detail.order.ordered_date != today:
            username = detail.order.user.username
            dishData = Ordered_Dishes_Ingredients_Details.objects.filter(ordered_dish_id=detail.id)
            for ingredientData in dishData:
                ingredientQuantityRelation = [str(ingredientData.ingredient), ingredientData.quantity]
                dishIngredients.append(ingredientQuantityRelation)
            dishData = [str(detail.ordered_dish),dishIngredients]
        data = {username: dishData}
        resultData.append(data)
    context = {'data': resultData}
    return render(request, 'show-orders.html', context)

def my_order(request):
    resultData=[]
    today = date.today().strftime("%Y-%m-%d")
    context = {}
    dishIngredients = []
    dishData = []
    username=''
    currentUserId = request.user.id
    ordersDetails = Ordered_Dishes.objects.all()
    for detail in ordersDetails:
        if detail.order.user.id == currentUserId:
            dishIngredients = []
            if detail.order.ordered_date == today:
                username = detail.order.user.username
                dishData = Ordered_Dishes_Ingredients_Details.objects.filter(ordered_dish_id=detail.id)
                for ingredientData in dishData:
                    ingredientQuantityRelation = [str(ingredientData.ingredient), ingredientData.quantity]
                    dishIngredients.append(ingredientQuantityRelation)
                dishData = [str(detail.ordered_dish),dishIngredients]
            data = {username: dishData}
            resultData.append(data)
    context = {'data': resultData}
    return render(request, 'show-orders.html', context)

@autheticated_user
@admin_permissions
def generatePDF(self):
    with open(settings.BASE_DIR +'/pdf2/Menu', errors="ignore") as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
    return response

@autheticated_user
@admin_permissions
def send_menu_by_slack(self):
    return tasks.send_menu_by_slack_task()

