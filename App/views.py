from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, View
import datetime
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.db.models import Q
from . models import Property,Article,Comparison,UserProfile

class IndexListView(ListView):
    model = Property
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super(IndexListView, self).get_context_data(**kwargs)
        if self.request.GET.get('first_check')=="one":
            query = self.request.GET.get('search')
            sale= self.request.GET.get('sale')
            rent= self.request.GET.get('rent')
            shortlet= self.request.GET.get('shortlet')
            hotel= self.request.GET.get('hotel')
            category= self.request.GET.get('category')
            min_price= self.request.GET.get('min_price')
            max_price=self.request.GET.get('max_price')
            if max_price:
                new_max=int(max_price)
            else:
                new_max="10000000000"
            if min_price:
                new_min=int(min_price)
            else:
                new_min=20
            if query:
                search = self.model.objects.filter(Q(address__icontains=query), Q(sale_type=sale) | Q(sale_type=rent) | Q(sale_type=shortlet) | Q(sale_type=hotel), Q(category=category),Q(price__lte=new_max))
                context['search'] = search
            else:
                search = self.model.objects.none()
                context['search'] = search
        elif self.request.GET.get('second_check')=="two":
            title=self.request.GET.get('title')
            address=self.request.GET.get('address')
            date=self.request.GET.get('date')
            category=self.request.GET.get('category')
            sale_type=self.request.GET.get('sale_type')
            price=self.request.GET.get('price')
            price_per_unit=self.request.GET.get('price_per_unit')
            image=self.request.GET.get('image')
            print(image)
            image_url=image.replace('/media/','')
            area=self.request.GET.get('area')
            rooms=self.request.GET.get('rooms')
            bedrooms=self.request.GET.get('bedrooms')
            bathrooms=self.request.GET.get('bathrooms')
            features=self.request.GET.get('features')
            building_age=self.request.GET.get('building_age')
            parking=self.request.GET.get('parking')
            cooling=self.request.GET.get('cooling')
            heating=self.request.GET.get('heating')
            sewer=self.request.GET.get('sewer')
            water=self.request.GET.get('water')
            exercise_room=self.request.GET.get('exercise_room')
            storage_room=self.request.GET.get('storage_room')
            request.session['compare'] = Comparison.objects.all()
            compare_check=Comparison.objects.filter(title=title,address=address,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
            area=area,rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
            water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
            if compare_check:
                pass
            else:
                compare=Comparison.objects.create(title=title,address=address,date=date,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                area=area,rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                compare.save()
            compare_count=Comparison.objects.filter(creator=self.request.user).count()
            if compare_count>3:
                compare_delete=Comparsion.objects.filter(creator=self.request.user)[4:]
                compare_delete.delete()
            else:
                pass
        check_login=self.request.user
        context['houses'] = Property.objects.all()[:6]
        context['articles'] = Article.objects.all()[:3]
        context['newyork'] = Property.objects.filter(Q(address__icontains="newYork")).count()
        context['losangeles'] = Property.objects.filter(Q(address__icontains="losangeles")).count()
        context['sanfransisco'] = Property.objects.filter(Q(address__icontains="sanfransisco")).count()
        context['miami'] = Property.objects.filter(Q(address__icontains="miami")).count()
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
        else:
            pass

        return context

def login_register(request):
    if request.method == 'POST':
        if request.POST.get("check")=="False":
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("index.html")
            else:
                return render(request, 'login-register.html', {"message": "The user does not exist"})
        elif request.POST.get("check")=="True":
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():

                    context = {"messages": "email already exists"}
                else:
                    user = User.objects.create(
                        username=username, password=password1, email=email)
                    user.set_password(user.password)
                    user.save()
                    profile = UserProfile.objects.create(user=user, username=username,email=email)
                    profile.save()
                    context = {"messages": "User Added"}
                    return render(request,'login-register.html',context)
        else:
            return render(request,'login-register.html')
    return render(request, "login-register.html")


def logout(request):
    auth.logout(request)
    return redirect("index.html")
