# Generated by Django 2.2.4 on 2020-08-22 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0014_auto_20200822_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='building_age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
