from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
# Create your models here.

class Newsletter(models.Model):
    name=models.TextField(blank=True, null=True)
    email=models.TextField(blank=True, null=True)
    phone=models.TextField(blank=True, null=True)

class Images(models.Model):
    title =models.TextField()
    image = models.ImageField()

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
    date=models.DateField(auto_now_add=True)
    category=models.TextField(blank=True, null=True)
    sale_type=models.TextField(blank=True, null=True)
    price=models.IntegerField(blank=True, null=True)
    price_per_unit = models.TextField(blank=True, null=True)
    agency = models.TextField(blank=True, null=True)
    developer = models.TextField(blank=True, null=True)
    image_1 = models.ManyToManyField(Images)
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
    name= models.TextField(blank=True, null=True)
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
    date=models.DateField(auto_now_add=True)
    summmary=models.TextField(blank=True, null=True)
    body=models.TextField(blank=True, null=True)
    author=models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    author_description = models.TextField(blank=True, null=True)
    author_image =  models.ImageField(blank=True, null=True)
    slug = models.SlugField()
    paginate_by = 2

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
    date=models.DateField(auto_now_add=True)
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
    image=  models.ImageField(blank=True, null=True)
    name=models.CharField(max_length=100, null=True,blank=True)
    title=models.TextField(blank=True, null=True)
    phone=models.TextField(blank=True, null=True)
    about=models.TextField(blank=True, null=True)
    twitter=models.TextField(blank=True, null=True)
    facebook=models.TextField(blank=True, null=True)
    google=models.TextField(blank=True, null=True)
    linkedin=models.TextField(blank=True, null=True)
    trials=models.IntegerField()
    email_confirmed = models.BooleanField(default=False)



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
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Agency(models.Model):
    title=models.TextField(blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    description=models.TextField(blank=True, null=True)
    phone=models.TextField(blank=True, null=True)
    email=models.TextField(blank=True, null=True)
    image=models.ImageField()
    slug = models.SlugField()
    paginate_by = 2

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("APP:agencies", kwargs={
            'slug': self.slug
        })
class Developer(models.Model):
    title=models.TextField(blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    description=models.TextField(blank=True, null=True)
    phone=models.TextField(blank=True, null=True)
    email=models.TextField(blank=True, null=True)
    image=models.ImageField()
    slug = models.SlugField()
    paginate_by = 2

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("APP:developers", kwargs={
            'slug': self.slug
        })

class Partner(models.Model):
    title=models.TextField(blank=True, null=True)
    image=models.ImageField()
    url = models.CharField(max_length = 200)
    paginate_by = 2

    def __str__(self):
        return self.title

class Boost(models.Model):
    title=models.TextField()
    image=models.ImageField()
    address=models.TextField(blank=True, null=True)
    category=models.TextField(blank=True, null=True)
    sale_type=models.TextField(blank=True, null=True)
    date=models.DateField(auto_now_add=True)
    expire=models.DateField()
    area = models.TextField(blank=True, null=True)
    rooms = models.TextField(blank=True, null=True)
    bedrooms = models.TextField(blank=True, null=True)
    bathrooms = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    price_per_unit = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    time=models.TextField()
    creator = models.ForeignKey(User, null=True,blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Agent(models.Model):
    name=models.TextField(blank=True, null=True)
    agency=models.TextField(blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    description=models.TextField(blank=True, null=True)
    phone=models.TextField(blank=True, null=True)
    email=models.TextField(blank=True, null=True)
    facebook=models.TextField(blank=True, null=True)
    twitter=models.TextField(blank=True, null=True)
    image=models.ImageField()
    slug = models.SlugField()
    paginate_by = 2

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("APP:agents", kwargs={
            'slug': self.slug
        })

class Bookmark(models.Model):
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
    date=models.DateField(auto_now_add=True)
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

class Valuation(models.Model):
    answer = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    type= (
        ('Public', 'Public'),
        ('City', 'City'),
    )
    address=models.TextField(blank=True, null=True)
    date=models.DateField(auto_now_add=True)
    category=models.TextField(blank=True, null=True)
    sale_type=models.TextField(blank=True, null=True)
    price=models.IntegerField(blank=True, null=True)
    price_per_unit = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
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
    user = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
