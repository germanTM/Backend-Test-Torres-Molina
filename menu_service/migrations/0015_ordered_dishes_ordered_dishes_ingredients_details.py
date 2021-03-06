# Generated by Django 3.0.8 on 2021-05-22 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu_service', '0014_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordered_Dishes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_service.Order')),
                ('ordered_dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_service.Dish')),
            ],
        ),
        migrations.CreateModel(
            name='Ordered_Dishes_Ingredients_Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_service.Ingredient')),
                ('ordered_dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_service.Ordered_Dishes')),
            ],
        ),
    ]
