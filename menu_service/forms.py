from django import forms
import datetime
from django.forms.widgets import Widget
from django.contrib import messages
from .models import Meal_Options_Dishes, Menu, Menu_Meal_Options, Ordered_Dishes, Ordered_Dishes_Ingredients_Details, Ingredient, Dish, Meal_Option, Daily_Menu, Dish_Ingredient, Order

class CreateIngredientForm(forms.Form):
    name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[a-z ]+', 'title':'Enter lower case characters only '}))

    def save(request):
        ingredientName = request.POST.get('name')
        existingIngredient = Ingredient.objects.filter(name=ingredientName).exists()
        if existingIngredient:
            return {'error':1, 'message':'Ingredient already exists'}
        else:
            try:
                Ingredient.objects.create(name=ingredientName)
                return {'error':0, 'message':''}
            except Exception as e:
                return {'error':1, 'message':str(e)}

class CreateDishForm(forms.Form):
    name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[a-z ]+', 'title':'Enter lower case characters only '}))
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)

    def save(request):
        ingredients = dict(request.POST)['ingredients']
        dishName = request.POST.get('name')
        existingDish = Dish.objects.filter(name=dishName).exists()
        if existingDish:
            return {'error':1, 'message':'Dish already exists'}
        else:
            try:
                savedDish = Dish.objects.create(name=dishName)
                dishId = savedDish.id
                for item in ingredients:
                    dishIngredient = Dish_Ingredient(dish_id = dishId, ingredient_id = item)
                    dishIngredient.save()
                return {'error':0, 'message':''}
            except Exception as e:
                return {'error':1, 'message':str(e)}

class CreateMealOptionForm(forms.Form):
    name = forms.CharField(required=True, max_length=30)
    dishes = forms.ModelMultipleChoiceField(queryset=Dish.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)

class CreateMenuForm(forms.Form):
    name = forms.CharField(required=True, max_length=30)
    scheduled_date = forms.DateField(initial=datetime.date.today)
    week_day = forms.ModelMultipleChoiceField(queryset=Daily_Menu.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)
    options = forms.ModelMultipleChoiceField(queryset=Meal_Option.objects.all(), widget=forms.CheckboxSelectMultiple(), required=True)

    def save(request, menu_id=0):
        registeredDate = False
        options = dict(request.POST)['options']
        menuName = request.POST.get('name')
        menuDate = request.POST.get('scheduled_date')
        menuWeekDay = dict(request.POST)['week_day']
        existingMenu = Menu.objects.filter(id=menu_id) if menu_id else Menu.objects.filter(name=menuName)
        try:
            if existingMenu:
                if str(existingMenu.first().scheduled_date) != str(menuDate): 
                    registeredDate = Menu.objects.filter(scheduled_date = menuDate).exists()
                if registeredDate:
                   return {'error':1, 'message':'There is a menu registered at that date'}
                else:
                    menu_id = existingMenu.first().id
                    existingMenu.update(scheduled_date = menuDate, name = menuName)
                    menuDishRelation = Menu_Meal_Options.objects.filter(menu_id=menu_id).all()
                    if menuDishRelation:
                        menuDishRelation.delete()
                        if options:
                            for option in options:
                                Menu_Meal_Options(menu_id=menu_id, meal_option_id=option).save()
                        if menuWeekDay:
                            for weekChoice in menuWeekDay:
                                saveMenuDay = Daily_Menu.objects.filter(id=weekChoice)
                                saveMenuDay.update(menu_id=menu_id)
                        return {'error':0, 'message':''}
                    else:
                        return {'error':1, 'message':'Check your Menu options, there are no relations between them'}
                    
            else:    
                registeredDate = Menu.objects.filter(scheduled_date = menuDate).exists()
                if registeredDate:
                    return {'error':1, 'message':'There is a menu registered at that date'}
                else:
                    savedMenu = Menu.objects.create(name=menuName, scheduled_date=menuDate)
                    menuId = savedMenu.id
                    if options:
                        for option in options:
                            menuOption = Menu_Meal_Options(meal_option_id = option, menu_id = menuId)
                            menuOption.save()
                    if menuWeekDay:
                        for weekChoice in menuWeekDay:
                            saveMenuDay = Daily_Menu.objects.filter(id=weekChoice)
                            saveMenuDay.update(menu_id=menuId)
                    return {'error':0, 'message':''}
        except Exception as e:
            return {'error':1, 'message':str(e)}

class CustomizeIngredientsForm(forms.Form): 

    def __init__(self, option, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dishesInOption = Meal_Options_Dishes.objects.prefetch_related('dish').filter(meal_option_id=option)
        if dishesInOption:
            for item in dishesInOption:
                relationDishIngredient = Dish_Ingredient.objects.prefetch_related('dish').filter(dish_id=item.dish_id)
                for dishIngredientItem in relationDishIngredient:
                    field_name = 'data/'+str(item.dish_id)+'/'+str(dishIngredientItem.ingredient_id)
                    self.fields[field_name] = forms.CharField(label=str(item.dish)+" - "+str(dishIngredientItem.ingredient),required=False, initial=1)

    def save(self, data, option, request):
        savedOrder = Order.objects.create(option_id = option, user_id=request.user.id)
        orderId = savedOrder.id
        orderedDish = 1
        orderedIngredient = 2
        orderedQuantity = 3
        processedDishes = []
        productsToProcess = []
        for key, value in data.items():
            if str(key).startswith('data/'):
                toInsetData = str(key)+'/'+str(value)
                dishIngredientRequest = str(toInsetData).split('/') 
                productsToProcess.append(dishIngredientRequest)
        for products in productsToProcess:
            dishId = Dish.objects.get(pk = products[orderedDish])
            ingredientId = Ingredient.objects.get(pk = products[orderedIngredient])
            if products[orderedDish] not in processedDishes: 
                saveOrderedDishes = Ordered_Dishes.objects.create(ordered_dish=dishId, order_id=orderId)

                processedDishes.append(products[orderedDish])
            Ordered_Dishes_Ingredients_Details(ordered_dish=saveOrderedDishes, ingredient=ingredientId, quantity=products[orderedQuantity]).save()
        
