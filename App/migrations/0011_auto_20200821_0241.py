# Generated by Django 2.2.4 on 2020-08-21 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0010_property_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comparison',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('category', models.TextField(blank=True, null=True)),
                ('sale_type', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('price_per_unit', models.TextField(blank=True, null=True)),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='')),
                ('area', models.TextField(blank=True, null=True)),
                ('rooms', models.TextField(blank=True, null=True)),
                ('bedrooms', models.TextField(blank=True, null=True)),
                ('bathrooms', models.TextField(blank=True, null=True)),
                ('features', models.TextField(blank=True, null=True)),
                ('building_age', models.TextField(blank=True, null=True)),
                ('parking', models.TextField(blank=True, null=True)),
                ('cooling', models.TextField(blank=True, null=True)),
                ('heating', models.TextField(blank=True, null=True)),
                ('sewer', models.CharField(blank=True, choices=[('Public', 'Public'), ('City', 'City')], max_length=100, null=True)),
                ('water', models.CharField(blank=True, choices=[('Public', 'Public'), ('City', 'City')], max_length=100, null=True)),
                ('exercise_room', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=100, null=True)),
                ('storage_room', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=100, null=True)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
