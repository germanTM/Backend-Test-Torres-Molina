from django.http import request
from django.test import TestCase, testcases
from .models import Daily_Menu, Ingredient, Dish, Meal_Option, Menu
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client, RequestFactory
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory, force_authenticate
import pytest
# Create your tests here.
class IngredientViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'nora',
            'password': 'secret'}
        User.objects.create_superuser(**self.credentials)
        self.ingredient = Ingredient()
        self.ingredient = Ingredient.objects.create(name="ajo")
        
    def test_create_ingredient(self):
        self.user = User.objects.first()
        self.client.force_login(self.user)
        ingredient_request = {'name': 'test ingredient'}
        response = self.client.post(f'/createIngredient', ingredient_request)
        self.assertEqual(response.status_code, 201)

    def test_ingredient_already_exists(self):
        self.user = User.objects.first()
        self.client.force_login(self.user)
        ingredient_request = {'name': 'ajo'}
        response = self.client.post(f'/createIngredient', ingredient_request)
        self.assertEqual(response.status_code, 400)

    def tearDown(self) -> None:
        return super().tearDown()

class CreateDishView(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'nora',
            'password': 'secret'}
        User.objects.create_superuser(**self.credentials)
        self.dish = Dish()
        self.dish = Dish.objects.create(name="pizza")
        self.ingredient = Ingredient()
        self.ingredient = Ingredient.objects.create(name="ajo")
        self.ingredient = Ingredient.objects.create(name="sal")
        self.ingredient = Ingredient.objects.create(name="pimienta")

    def test_create_new_dish(self):
        self.user = User.objects.first()
        self.client.force_login(self.user)
        create_dish_request = {'name': 'tacos', 'ingredients': ['1','2', '3']}
        response = self.client.post(f'/createDish', create_dish_request)
        self.assertEqual(response.status_code, 201)
    
    def test_new_dish_unknown_ingredient(self):
        self.user = User.objects.first()
        self.client.force_login(self.user)
        create_dish_request = {'name': 'sushi', 'ingredients': ['10','11','12']}
        response = self.client.post(f'/createDish', create_dish_request)
        self.assertEqual(response.status_code, 400)

    def tearDown(self) -> None:
        return super().tearDown()

class CreateMenuView(TestCase):
    def setUp(self):
        self.client = Client()
        self.credentials = {
            'username': 'nora',
            'password': 'secret'}
        User.objects.create_superuser(**self.credentials)
        self.dailyMenu = Daily_Menu.objects.create(name="Jueves",menu_id=None)
        self.options = Meal_Option()
        self.option = Meal_Option.objects.create(name="Opcion 1")
        self.dish = Menu()
        self.dish = Menu.objects.create(name="menu 1", scheduled_date="2021-05-23")
        
    def test_create_menu(self):
        self.user = User.objects.first()
        self.client.force_login(self.user)
        create_menu_request = {
            'name':"menu 2", 
            'scheduled_date':"2021-05-22",
            'week_day':"1",
            'options':"1"
        }
        response = self.client.post(f'/createMenu', create_menu_request)
        self.assertEqual(response.status_code, 201)
        
    def test_create_menu_existing_date(self):
        self.user = User.objects.first()
        self.client.force_login(self.user)
        create_menu_request = {
            'name':"menu 3", 
            'scheduled_date':"2021-05-23",
            'week_day':"1",
            'options':"1"
        }
        response = self.client.post(f'/createMenu', create_menu_request)
        self.assertEqual(response.status_code, 400)

        def tearDown(self) -> None:
            return super().tearDown()

class MenuForOrderView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.credentials = {
            'username': 'nora',
            'password': 'secret'}
        User.objects.create_superuser(**self.credentials)

    def create_simple_order(self):
        self.user = User.objects.first()
        self.client.force_login(self.user)
        response = self.client.get(f'/menuOptions')
        self.assertEqual(response.status_code, 302)

