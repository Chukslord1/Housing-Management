# Generated by Django 2.2.4 on 2020-08-23 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0017_property_agency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='first_floor',
        ),
        migrations.RemoveField(
            model_name='property',
            name='first_floor_description',
        ),
        migrations.RemoveField(
            model_name='property',
            name='second_floor',
        ),
        migrations.RemoveField(
            model_name='property',
            name='second_floor_description',
        ),
        migrations.RemoveField(
            model_name='property',
            name='third_floor',
        ),
        migrations.RemoveField(
            model_name='property',
            name='third_floor_description',
        ),
    ]
