# Generated by Django 3.0.8 on 2021-05-19 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_service', '0005_auto_20210519_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal_Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]
