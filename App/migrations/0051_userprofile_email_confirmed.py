# Generated by Django 2.2.4 on 2020-09-08 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0050_boost_expire'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
