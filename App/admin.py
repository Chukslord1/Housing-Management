from django.contrib import admin
from . models import Property,Article,Comparison,UserProfile
# Register your models here.


admin.site.register(Property)
admin.site.register(Article)
admin.site.register(Comparison)
admin.site.register(UserProfile)
