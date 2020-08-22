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
                new_max=10000000000
            if min_price:
                new_min=int(min_price)
            else:
                new_min=20
            if query:
                search = self.model.objects.filter(Q(address__icontains=query), Q(sale_type=sale) | Q(sale_type=rent) | Q(sale_type=shortlet) | Q(sale_type=hotel) | Q(sale_type__icontains="e"), Q(category__icontains=category),Q(price__lte=new_max))
                context['search'] = search
            else:
                search = self.model.objects.none()
                context['search'] = search
        elif self.request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=self.request.user)
            clear.delete()
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

def submit_property(request):
    return render(request,"submit-property.html")


class SearchListView(ListView):
    model = Property
    template_name = "listings-list-full-width.html"
    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        if self.request.GET.get('first_check')=="one":
            query = self.request.GET.get('search')
            sale= self.request.GET.get('sale')
            rent= self.request.GET.get('rent')
            shortlet= self.request.GET.get('shortlet')
            hotel= self.request.GET.get('hotel')
            category= self.request.GET.get('category')
            max_price=self.request.GET.get('max_price')
            if max_price:
                new_max=int(max_price)
            else:
                new_max=10000000000
            if query:
                search = self.model.objects.filter(Q(address__icontains=query), Q(sale_type=sale) | Q(sale_type=rent) | Q(sale_type=shortlet) | Q(sale_type=hotel) | Q(sale_type__icontains="e"), Q(category__icontains=category),Q(price__lte=new_max))
                context['search'] = search
            else:
                search = self.model.objects.none()
                context['search'] = search
        elif self.request.GET.get('realcheck')=="True":
            query = self.request.GET.get('search')
            sale_type=self.request.GET.get('sale_type')
            category = self.request.GET.get('category')
            min_area_1 = self.request.GET.get('min_area_1')
            max_area_1 = self.request.GET.get('max_area_1')
            min_price_1 = self.request.GET.get('min_price_1')
            max_price_1 = self.request.GET.get('max_price_1')
            min_area_2=min_area_1.replace("+","")
            max_area_2=max_area_1.replace("+","")
            min_price_2=min_price_1.replace("+","")
            max_price_2=max_price_1.replace("+","")
            min_area=min_area_1.replace(" ","")
            max_area=max_area_1.replace(" ","")
            min_price=min_price_1.replace(" ","")
            max_price=max_price_1.replace(" ","")
            building_age_1 = self.request.GET.get('building_age')
            if building_age_1:
                building_age=int(building_age_1)
            else:
                building_age=building_age_1
            bedrooms_1 = self.request.GET.get('bedrooms')
            if bedrooms_1:
                bedrooms=int(bedrooms_1)
            else:
                bedrooms=bedrooms_1
            rooms_1 = self.request.GET.get('rooms')
            if rooms_1:
                rooms=int(rooms_1)
            else:
                rooms=rooms_1
            bathrooms_1 = self.request.GET.get('bathrooms')
            if bathrooms_1:
                bathrooms=int(bathrooms_1)
            else:
                bathrooms=bathrooms_1
            if max_price:
                new_max=int(max_price)
            else:
                new_max=10000000000
            if max_area:
                new_max_area=int(max_area)
            else:
                new_max_area=10000000000
            if query:
                zero=0
                search = self.model.objects.filter(Q(address__icontains=query), Q(sale_type=sale_type) | Q(sale_type__icontains="e"), Q(category__icontains=category),Q(price__lte=new_max),Q(area__lte=new_max_area) | Q(area__lte=100000),Q(building_age__gte=zero),Q(bedrooms__gte=zero),Q(rooms__gte=zero),Q(bathrooms__gte=zero))
                context['search'] = search
            else:
                search = self.model.objects.none()
                context['search'] = search
        elif self.request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=self.request.user)
            clear.delete()
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
            compare_check=Comparison.objects.filter(title=title,address=address,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
            rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
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


def category(request):
    return render(request,"listings-grid-standard-with-sidebar.html")

def popular(request):
    return render(request,"listings-list-with-sidebar.html")


def compare(request):
    return render(request,"compare-properties.html")

class PropertyDetailView(DetailView):
    model = Property
    template_name = "single-property-page-1.html"

    def get_context_data(self, **kwargs):
        context = super(PropertyDetailView, self).get_context_data(**kwargs)


        check_login=self.request.user
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
        else:
            pass


        return context
