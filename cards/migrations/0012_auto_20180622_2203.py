# Generated by Django 2.0.6 on 2018-06-22 22:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0011_cardsequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardrating',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 22, 22, 3, 35, 590434)),
        ),
        migrations.AddField(
            model_name='cardsequence',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 22, 22, 3, 35, 593665)),
        ),
    ]
