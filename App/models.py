from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
# Create your models here.
class Property(models.Model):
    title=models.TextField(blank=True, null=True)
    answer = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    type= (
        ('Public', 'Public'),
        ('City', 'City'),
    )
    address=models.TextField(blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    category=models.TextField(blank=True, null=True)
    sale_type=models.TextField(blank=True, null=True)
    price=models.IntegerField(blank=True, null=True)
    price_per_unit = models.TextField(blank=True, null=True)
    agency = models.TextField(blank=True, null=True)
    image_1 = models.ImageField(blank=True, null=True)
    image_2 = models.ImageField(blank=True, null=True)
    image_3 = models.ImageField(blank=True, null=True)
    image_4 = models.ImageField(blank=True, null=True)
    image_5 = models.ImageField(blank=True, null=True)
    image_6 = models.ImageField(blank=True, null=True)
    image_7 = models.ImageField(blank=True, null=True)
    area = models.IntegerField(blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True)
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    building_age = models.IntegerField(blank=True, null=True)
    parking = models.TextField(blank=True, null=True)
    cooling = models.TextField(blank=True, null=True)
    heating = models.TextField(blank=True, null=True)
    sewer = models.CharField(max_length = 100, choices = type,blank=True, null=True)
    water = models.CharField(max_length = 100, choices = type,blank=True, null=True)
    exercise_room = models.CharField(max_length = 100, choices = answer,blank=True, null=True)
    storage_room = models.CharField(max_length = 100, choices = answer,blank=True, null=True)
    video = models.FileField(blank=True, null=True)
    creator = models.TextField(blank=True, null=True)
    slug = models.SlugField()
    paginate_by = 2

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("APP:details", kwargs={
            'slug': self.slug
        })


class Article(models.Model):
    title=models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    summmary=models.TextField(blank=True, null=True)
    body=models.TextField(blank=True, null=True)
    author=models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    author_description = models.TextField(blank=True, null=True)
    author_image =  models.ImageField(blank=True, null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("APP:blog", kwargs={
            'slug': self.slug
        })

class Comparison(models.Model):
    title=models.TextField(blank=True, null=True)
    answer = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    type= (
        ('Public', 'Public'),
        ('City', 'City'),
    )
    address=models.TextField(blank=True, null=True)
    date=models.DateTimeField(auto_now_add=True)
    category=models.TextField(blank=True, null=True)
    sale_type=models.TextField(blank=True, null=True)
    price=models.IntegerField(blank=True, null=True)
    price_per_unit = models.TextField(blank=True, null=True)
    image_1 = models.ImageField(blank=True, null=True)
    area = models.IntegerField(blank=True, null=True)
    rooms = models.IntegerField(blank=True, null=True)
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    building_age = models.IntegerField(blank=True, null=True)
    parking = models.TextField(blank=True, null=True)
    cooling = models.TextField(blank=True, null=True)
    heating = models.TextField(blank=True, null=True)
    sewer = models.CharField(max_length = 100, choices = type,blank=True, null=True)
    water = models.CharField(max_length = 100, choices = type,blank=True, null=True)
    exercise_room = models.CharField(max_length = 100, choices = answer,blank=True, null=True)
    storage_room = models.CharField(max_length = 100, choices = answer,blank=True, null=True)
    creator = models.ForeignKey(User, null=True,blank=True, on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    username=models.CharField(max_length=100, null=True,blank=True)
    email=models.CharField(max_length=100, null=True,blank=True)

class Tour(models.Model):
    user= models.ForeignKey(User, null=True,blank=True, on_delete=models.CASCADE)
    time =models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    property = models.TextField(blank=True, null=True)
    phone =models.TextField(blank=True, null=True)
    name =models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
class Comment(models.Model):
    name=models.TextField(blank=True, null=True)
    email=models.TextField(blank=True, null=True)
    comment=models.TextField(blank=True, null=True)
    blog = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
