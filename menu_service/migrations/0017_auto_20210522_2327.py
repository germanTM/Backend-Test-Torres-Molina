# Generated by Django 3.0.8 on 2021-05-22 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_service', '0016_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
