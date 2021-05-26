from django.shortcuts import render, redirect
from  .models import Meal_Option, Meal_Options_Dishes, Menu, Ordered_Dishes_Ingredients_Details
from django.contrib import messages
from .decorators.decorators import admin_permissions, autheticated_user, autheticated_user
from datetime import *
from django.http import HttpResponse
from django.conf import settings
from . import tasks
from django.views import View

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
                messages.success(request, "Error creating message: Motive: "+ingredientCreation.get('message'))
                return render(request, "create-ingredient.html", context, status=400)
            else:
                messages.success(request, "Ingredient created succesfully")
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
        context = {'form':form}
        if form.is_valid():
            dishes = dict(request.POST)['dishes']
            optionName = request.POST.get('name')
            existingOption = Meal_Option.objects.filter(name=optionName)
            if existingOption:
                messages.info(request, "Option is already registered")
                return render(request, "create-meal-option.html", context, status=400)
            else:
                savedOption = Meal_Option.objects.create(name=optionName)
                optionId = savedOption.id
                for item in dishes:
                    dishOption = Meal_Options_Dishes(dish_id = item, meal_option_id = optionId)
                    dishOption.save()
                messages.info(request, "Option created succesfully")
                return render(request, "create-meal-option.html", context, status=200)
        messages.info(request, "Create meal option form is incorrect")
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
                messages.info(request, "Menu created succesfully")
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
    if listMenu.count() > 0:
        context = {'menus':listMenu}
        return render(request, 'list-menus.html', context)
    messages.info(request, "There are no menus available")
    return render(request, 'list-menus.html', context)

@autheticated_user
@admin_permissions
def menu_details(request, menu_id = 0):
    menuDetails = functions.menu_details(request, menu_id)
    if  menuDetails.get('error') == 1:
        messages.info(request, "Error displaying menu details, motive: "+menuDetails.get('message'))
    else:
        context = {'optionDishRelation': menuDetails.get('optionDishRelation'), 'dishesIngredients':menuDetails.get('dishesIngredients'), 'dishOptionRelation':menuDetails.get('dishOptionRelation')}
        return render(request, 'list-menu-options.html', context, status=200)
    return redirect('home')

@autheticated_user
def show_menu_for_order(request):
    onTime = functions.get_limit_hour_for_order(settings.CHILE_TIME_ZONE)
    onTime = True
    if onTime:
        menuDetails = functions.menu_details(request)
        if menuDetails.get('error') == 1:
            messages.info(request, "Error displaying menu details, motive: "+menuDetails.get('message'))
        else:
            context = {'optionDishRelation': menuDetails.get('optionDishRelation'), 'dishesIngredients':menuDetails.get('dishesIngredients'), 'dishOptionRelation':menuDetails.get('dishOptionRelation')}
            return render(request, 'list-menu-of-the-day.html', context, status=200)
    else:
        messages.info(request, "The time for ordering has finished: ")
        return redirect('home')
    return redirect('home')

@autheticated_user
def view_ingredients(request, option):
    form = CustomizeIngredientsForm(option)
    if request.method == 'POST':
        formRequest = request.POST
        form.save(formRequest, option, request)
        messages.info(request, "Order successfully created")
        return redirect('home')
    context={"form": form}
    return render(request, 'customize-ingredients.html', context)

@autheticated_user
@admin_permissions
def view_orders(request):
    status=200
    today = date.today().strftime("%Y-%m-%d")
    ordersDetails = Ordered_Dishes_Ingredients_Details.objects.filter(ordered_dish__order__ordered_date=today).prefetch_related('ingredient','ordered_dish')
    if ordersDetails.count() <= 0:
        status=400
        messages.info(request, "There are no orders for today")
    context = {'data': ordersDetails}
    return render(request, 'show-orders.html', context, status=status)

@autheticated_user
def my_order(request):
    status=200
    currentUserId = request.user.id
    today = date.today().strftime("%Y-%m-%d")
    ordersDetails = Ordered_Dishes_Ingredients_Details.objects.filter(ordered_dish__order__ordered_date=today, ordered_dish__order__user=currentUserId).prefetch_related('ingredient','ordered_dish')
    if ordersDetails.count() <= 0:
        status=400
        messages.info(request, "There are no orders for today")
    context = {'data': ordersDetails}
    return render(request, 'show-orders.html', context, status=status)

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

