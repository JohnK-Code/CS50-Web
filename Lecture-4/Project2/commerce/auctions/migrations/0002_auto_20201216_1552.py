# Generated by Django 3.1.1 on 2020-12-16 15:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Modern', 'Modern'), ('Classic', 'Classic'), ('American', 'American')], max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='endTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 23, 15, 52, 40, 636436)),
        ),
    ]