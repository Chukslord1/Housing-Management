# Generated by Django 2.2.4 on 2020-08-25 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0028_agent_agency'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
