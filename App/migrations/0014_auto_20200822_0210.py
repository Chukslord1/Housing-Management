# Generated by Django 2.2.4 on 2020-08-22 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comparison',
            name='area',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='area',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
