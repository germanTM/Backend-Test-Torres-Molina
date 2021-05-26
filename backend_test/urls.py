"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls import *
from accounts import views as va
from menu_service import views as vm
from .utils.healthz import healthz
from django.conf import settings
import os

urlpatterns = [
    path("login", va.loginPage, name="login"),
    path("logout", va.logoutUser, name="logout"),
    path("home", va.homePage, name="home"),
    path("register", va.register, name="register"),
    path("createIngredient", vm.create_ingredient, name="create_ingredient"),
    path("createDish", vm.create_dish, name="create_dish"),
    path("createMealOption", vm.create_meal_option, name="create_meal_option"),
    path("listMenu", vm.list_menu, name="list_menu"),
    path('menuDetails/<menu_id>/', vm.menu_details, name='menu_details'),
    path("healthz", healthz, name="healthz"),
    url(r'^createMenu', vm.create_menu, name="create_menu"),
    url(r'^createMenu/(?P<menu_id>\w+)/$', vm.create_menu, name="create_menu"),
    path("viewIngredients/<option>", vm.view_ingredients, name="view_ingredients"),
    path('menuDetails', vm.menu_details, name="menu_details"),
    path('menuOptions', vm.show_menu_for_order, name="show_menu_for_order"),
    path(os.path.join('generatePDF',settings.MENU_URL), vm.generatePDF, name="generate_pdf"),
    path('iniciateMessageSending', vm.send_menu_by_slack, name="send_menu_by_slack"),
    path('allOrders', vm.view_orders, name="all_orders"),
    path('myOrder', vm.my_order, name="my_order"),
]
