# Generated by Django 3.0.8 on 2021-05-19 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu_service', '0003_dish_dishingredient'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DishIngredient',
            new_name='Dish_Ingredient',
        ),
        migrations.RenameField(
            model_name='dish_ingredient',
            old_name='dishId',
            new_name='dish_Id',
        ),
        migrations.RenameField(
            model_name='dish_ingredient',
            old_name='ingredientId',
            new_name='ingredient_Id',
        ),
    ]
