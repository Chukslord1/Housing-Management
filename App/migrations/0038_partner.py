# Generated by Django 2.2.4 on 2020-09-01 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0037_auto_20200901_0150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='')),
                ('url', models.CharField(max_length=200)),
            ],
        ),
    ]
