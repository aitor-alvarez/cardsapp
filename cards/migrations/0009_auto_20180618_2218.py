# Generated by Django 2.0.6 on 2018-06-18 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0008_auto_20180618_2217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='chinese_description',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='russian_description',
        ),
    ]
