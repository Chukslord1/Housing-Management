# Generated by Django 2.2.4 on 2020-08-20 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_auto_20200820_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='sale_type',
            field=models.TextField(blank=True, null=True),
        ),
    ]
