# Generated by Django 2.2.4 on 2020-09-01 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0038_partner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
    ]
