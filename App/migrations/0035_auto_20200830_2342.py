# Generated by Django 2.2.4 on 2020-08-30 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0034_userprofile_trials'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.RemoveField(
            model_name='property',
            name='image_1',
        ),
        migrations.AddField(
            model_name='property',
            name='image_1',
            field=models.ManyToManyField(to='App.Images'),
        ),
    ]
