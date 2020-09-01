# Generated by Django 2.2.4 on 2020-09-01 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0035_auto_20200830_2342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Valuation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('category', models.TextField(blank=True, null=True)),
                ('sale_type', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('price_per_unit', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('area', models.IntegerField(blank=True, null=True)),
                ('rooms', models.IntegerField(blank=True, null=True)),
                ('bedrooms', models.IntegerField(blank=True, null=True)),
                ('bathrooms', models.IntegerField(blank=True, null=True)),
                ('features', models.TextField(blank=True, null=True)),
                ('building_age', models.IntegerField(blank=True, null=True)),
                ('parking', models.TextField(blank=True, null=True)),
                ('cooling', models.TextField(blank=True, null=True)),
                ('heating', models.TextField(blank=True, null=True)),
                ('sewer', models.CharField(blank=True, choices=[('Public', 'Public'), ('City', 'City')], max_length=100, null=True)),
                ('user', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
