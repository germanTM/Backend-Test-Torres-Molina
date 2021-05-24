from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.conf import settings
import uuid

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
            return self.name
class Dish(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
class Dish_Ingredient(models.Model):
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
class Meal_Option(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
class Meal_Options_Dishes(models.Model):
    meal_option = models.ForeignKey('Meal_Option', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
class Menu(models.Model):
    name = models.CharField(max_length=50)
    scheduled_date = models.DateField()
class Menu_Meal_Options(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    meal_option = models.ForeignKey('Meal_Option', on_delete=models.CASCADE)
    def __int__(self) -> int:
        return self.meal_option
class Daily_Menu(models.Model):
    name = models.CharField(max_length=50)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, null=True)
    def __str__(self) -> int:
        return self.name
class Order(models.Model):
    option = models.ForeignKey('Meal_option', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    ordered_date = models.DateField(auto_now_add=True)
    def __str__(self) -> int:
        return self.ordered_date
class Ordered_Dishes(models.Model):
    ordered_dish = models.ForeignKey('Dish', on_delete=models.CASCADE, null=False)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=False)
class Ordered_Dishes_Ingredients_Details(models.Model):
    ordered_dish = models.ForeignKey('Ordered_Dishes', on_delete=models.CASCADE, null=False)
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, null=False)
    quantity = models.IntegerField(null=False)
class Files(models.Model):
    id = models.UUIDField(primary_key=True, default=settings.MENU_URL, editable=False)
    name = models.FileField(upload_to='pdf2/')