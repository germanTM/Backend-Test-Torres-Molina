# Generated by Django 3.0.8 on 2021-05-23 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_service', '0017_auto_20210522_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='name',
            field=models.FileField(upload_to='pdf2/'),
        ),
    ]
