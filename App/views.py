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
from . models import Property,Article,Comparison,UserProfile,Tour,Comment,Agency,Agent
import random

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
            if self.request.user.is_authenticated:
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
                compare_count=Comparison.objects.filter(creator=self.request.user    ).count()
                if compare_count>3:
                    compare_delete=Comparsion.objects.filter(creator=self.request    .user)[4:]
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

class ArticleListView(ListView):
    model = Article
    template_name = "blog.html"
    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        if self.request.GET.get('comment_check')=="True":
            name=self.request.GET.get("name")
            email=self.request.GET.get("email")
            comment=self.request.GET.get("comment")
            new_comment=Comment.objects.create(name=name,email=email,comment=comment,blog=obj.title)
            new_comment.save()
        check_login=self.request.user
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
        else:
            pass

        context['blogs'] = Article.objects.all()
        popular=[]
        blog=Article.objects.all()
        check=1
        for i in blog:
            if Comment.objects.filter(blog=i.title):
                if Comment.objects.filter(blog=i.title).count() > check:
                    check=Comment.objects.filter(blog=i.title).count()
                    x = Article.objects.filter(title=i.title)
                    popular.append(x)
        context['popular'] = popular[0]
        if len(popular)>2:
            context['popular_2'] = popular[1]
            context['popular_3'] = popular[2]
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
    context={"agencies":Agency.objects.all(),"compare":Comparison.objects.all()}
    if request.method=="POST":
        title=request.POST.get("title")
        status=request.POST.get("status")
        category=request.POST.get("category")
        price_new=request.POST.get("price")
        if price_new:
            price=int(price_new)
        else:
            price=1000000
        price_per_unit_new=request.POST.get("price_per_unit")
        price_per_unit=int(price_per_unit_new)
        agency=request.POST.get("agency")
        area_new=request.POST.get("area")
        if area_new:
            area=int(area_new)
        else:
            area=40000
        rooms_new=request.POST.get("rooms")
        if rooms_new:
            rooms=int(rooms_new)
        else:
            roms=3
        image_1=request.FILES.get("image_1")
        image_2=request.FILES.get("image_2")
        image_3=request.FILES.get("image_3")
        image_4=request.FILES.get("image_4")
        image_5=request.FILES.get("image_5")
        image_6=request.FILES.get("image_6")
        image_7=request.FILES.get("image_7")
        address=request.POST.get("address")
        description=request.POST.get("description")
        building_age_new=request.POST.get("building_age")
        if building_age_new:
            building_age=int(building_age_new)
        else:
            building_age=3
        bedrooms_new=request.POST.get("bedrooms")
        if bedrooms_new:
            bedrooms=int(bedrooms_new)
        else:
            bedrooms=3
        bathrooms_new=request.POST.get("bathrooms")
        if bathrooms_new:
            bathrooms=int(bathrooms_new)
        else:
            bathrooms=3
        features=request.POST.get("features")
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        parking=request.POST.get("parking")
        cooling=request.POST.get("cooling")
        heating=request.POST.get("heating")
        sewer=request.POST.get("sewer")
        slug=title+status+address+price_new
        property_check=Property.objects.filter(title=title,address=address)
        if property_check:
            context={'message':"Property Already Exists","agencies":Agency.objects.all(),"compare":Comparison.objects.all()}
        else:
            property=Property.objects.create(title=title,sale_type=status,category=category,price=price,price_per_unit=price_per_unit,agency=agency,
            area=area,rooms=rooms,image_1=image_1,image_2=image_2,image_3=image_3,image_4=image_4,image_5=image_5,image_6=image_6,image_7=image_7,address=address,
            description=description,building_age=building_age,bedrooms=bedrooms,bathrooms=bathrooms,features=features,parking=parking,cooling=cooling,heating=heating,sewer=sewer,name=name,email=email,phone=phone,slug=slug)
            property.save()
            agent=Agent.object.create(name=name,phone=phone,email=email)
            agent.save()
            user_check=User.object.filter(email=email)
            if user_check:
                pass
            else:
                user=User.objects.create(username=name,password=name+"2020",email=email)
                user.save()
                message=request.POST['message']
                fromaddr = "housing-send@advancescholar.com"
                toaddr = email
                subject="Account Creation Details"
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = "Your account login details"


                body = "Your account login details are:"+" username: "+name+" password "+ password
                msg.attach(MIMEText(body, 'plain'))

                server = smtplib.SMTP('mail.advancescholar.com',  26)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login("housing-send@advancescholar.com", "housing@24hubs.com")
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
            context={"message":"Successfully Added Property"}
    elif request.method=="GET":
        if request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=request.user)
            clear.delete()
    return render(request,"submit-property.html",context)


class SearchListView(ListView):
    model = Property
    template_name = "listings-list-full-width.html"
    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        if self.request.GET.get('first_check')=="one":
            query = self.request.GET.get('search')
            tab= self.request.GET.get('tab')
            category= self.request.GET.get('category')
            max_price=self.request.GET.get('max_price')
            if max_price:
                new_max=int(max_price)
            else:
                new_max=10000000000
            if query:
                search = self.model.objects.filter(Q(address__icontains=query), Q(sale_type=tab) | Q(sale_type__icontains="e"), Q(category__icontains=category),Q(price__lte=new_max))
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
            if self.request.user.is_authenticated:
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
                compare_count=Comparison.objects.filter(creator=self.request.user    ).count()
                if compare_count>3:
                    compare_delete=Comparsion.objects.filter(creator=self.request    .user)[4:]
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


class CategoryListView(ListView):
    model = Property
    template_name = "listings-grid-standard-with-sidebar.html"
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        if self.request.GET.get('first_check')=="one":
            query = self.request.GET.get('search')
            if query:
                search = self.model.objects.filter(Q(address__icontains=query))
                context['search'] = search
            else:
                search = self.model.objects.none()
                context['search'] = search
        elif self.request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=self.request.user)
            clear.delete()
        elif self.request.GET.get('second_check')=="two":
            if self.request.user.is_authenticated:
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
                compare_count=Comparison.objects.filter(creator=self.request.user    ).count()
                if compare_count>3:
                    compare_delete=Comparsion.objects.filter(creator=self.request    .user)[4:]
                    compare_delete.delete()
                else:
                    pass
        check_login=self.request.user
        context['houses'] = Property.objects.all()[:6]
        context['articles'] = Article.objects.all()[:3]
        context['popular'] = Property.objects.filter(Q(category__icontains="house"))
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
        else:
            pass

        return context


class PopularListView(ListView):
    model = Property
    template_name = "listings-list-with-sidebar.html"
    def get_context_data(self, **kwargs):
        context = super(PopularListView, self).get_context_data(**kwargs)
        if self.request.GET.get('first_check')=="one":
            query = self.request.GET.get('search')
            if query:
                search = self.model.objects.filter(Q(address__icontains=query))
                context['search'] = search
            else:
                search = self.model.objects.none()
                context['search'] = search
        elif self.request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=self.request.user)
            clear.delete()
        elif self.request.GET.get('second_check')=="two":
            if self.request.user.is_authenticated:
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
                compare_count=Comparison.objects.filter(creator=self.request.user    ).count()
                if compare_count>3:
                    compare_delete=Comparsion.objects.filter(creator=self.request    .user)[4:]
                    compare_delete.delete()
                else:
                    pass
        check_login=self.request.user
        context['houses'] = Property.objects.all()[:6]
        context['articles'] = Article.objects.all()[:3]
        context['popular'] = Property.objects.filter(Q(address__icontains="Lagos"))
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
        else:
            pass

        return context


def compare(request):
    compare=Comparison.objects.all()
    context={"compare":compare}
    if request.GET.get('clear')=="True":
        clear=Comparison.objects.filter(creator=request.user)
        clear.delete()
        return redirect("compare-properties.html")
    return render(request,"compare-properties.html",context)

def contact(request):
    context={"compare":Comparison.objects.all()}
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        fromaddr = "housing-send@advancescholar.com"
        toaddr = "housing@advancescholar.com"
        subject=request.POST['subject']
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = name + "-" + subject


        body = message +"-"+"email" + email
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('mail.advancescholar.com',  26)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("housing-send@advancescholar.com", "housing@24hubs.com")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        context={'message':'Your message has been sent sucessfully',"compare":Comparison.objects.all()}
        return render(request, 'contact.html',context)
    elif request.method=="GET":
        if request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=request.user)
            clear.delete()
    return render(request,"contact.html",context)

class PropertyDetailView(DetailView):
    model = Property
    template_name = "single-property-page-1.html"

    def get_object(self, queryset=None):
        global obj
        obj = super(PropertyDetailView, self).get_object(queryset=queryset)
        print(obj)
        return obj
    def get_context_data(self, **kwargs):
        context = super(PropertyDetailView, self).get_context_data(**kwargs)
        if self.request.GET.get('second_check')=="two":
            if self.request.user.is_authenticated:
                title=self.request.GET.get('title')
                address=self.request.GET.get('address')
                date=self.request.GET.get('date')
                category=self.request.GET.get('category')
                sale_type=self.request.GET.get('sale_type')
                price=self.request.GET.get('price')
                price_per_unit=self.request.GET.get('price_per_unit')
                image=self.request.GET.get('image')
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
        elif self.request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=self.request.user)
            clear.delete()
        elif self.request.GET.get('tour')=="True":
            date=self.request.GET.get('date')
            time=self.request.GET.get('time')
            phone=self.request.GET.get('phone')
            name=self.request.GET.get('name')
            if self.request.user.is_authenticated:
                tour=Tour.objects.create(date=date,time=time,user=self.request.user,property=obj.title,phone=phone,name=name)
                tour.save()
            else:
                tour=Tour.objects.create(date=date,time=time,property=obj.title,phone=phone,name=name)
                tour.save()
        elif self.request.method=="POST":
            name=self.request.POST['name']
            email=self.request.POST['email']
            message=self.request.POST.get['message']
            fromaddr = "housing-send@advancescholar.com"
            toaddr = request.Post.get('to')
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] ="Enquiry For Property"


            body = message+ "my contacts are" +" phone: "+phone + " email " + email
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('mail.advancescholar.com',  26)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("housing-send@advancescholar.com", "housing@24hubs.com")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
        check_login=self.request.user
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
        else:
            pass
        context['houses'] = Property.objects.filter(sale_type=obj.sale_type,category=obj.category).exclude(title=obj.title)
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog-post.html"

    def get_object(self, queryset=None):
        global obj
        obj = super(ArticleDetailView, self).get_object(queryset=queryset)
        return obj
    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        if self.request.GET.get('comment_check')=="True":
            name=self.request.GET.get("name")
            email=self.request.GET.get("email")
            comment=self.request.GET.get("comment")
            new_comment=Comment.objects.create(name=name,email=email,comment=comment,blog=obj.title)
            new_comment.save()
        check_login=self.request.user
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
        else:
            pass

        context['related'] = Article.objects.filter(author=obj.author).exclude(title=obj.title)
        context['blogs'] = Article.objects.all()
        context['commment_no'] = Comment.objects.filter(blog=obj.title).count()
        context['comments'] = Comment.objects.filter(blog=obj.title)
        popular=[]
        blog=Article.objects.all()
        check=1
        for i in blog:
            if Comment.objects.filter(blog=i.title):
                if Comment.objects.filter(blog=i.title).count() > check:
                    check=Comment.objects.filter(blog=i.title).count()
                    x = Article.objects.filter(title=i.title)
                    popular.append(x)
        if len(popular)>0:
            context['popular'] = popular[0]
        if len(popular)>2:
            context['popular_2'] = popular[1]
            context['popular_3'] = popular[2]
        return context

class AgencyListView(ListView):
    model = Agency
    template_name = "agencies-list.html"
    def get_context_data(self, **kwargs):
        context = super(AgencyListView, self).get_context_data(**kwargs)
        if self.request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=self.request.user)
            clear.delete()
        context["compare"] = Comparison.objects.all()
        return context

class AgencyDetailView(DetailView):
    model = Agency
    template_name = "agency-page.html"

    def get_object(self, queryset=None):
        global obj
        obj = super(AgencyDetailView, self).get_object(queryset=queryset)
        return obj
    def get_context_data(self, **kwargs):
        context = super(AgencyDetailView, self).get_context_data(**kwargs)
        if self.request.GET.get('first_check')=="one":
            query = self.request.GET.get('search')
            if query:
                search = Property.filter(Q(address__icontains=query),Q(agency=obj.title))
                context['search'] = search
            else:
                search = self.model.objects.none()
                context['search'] = search
        if self.request.GET.get('second_check')=="two":
            if self.request.user.is_authenticated:
                title=self.request.GET.get('title')
                address=self.request.GET.get('address')
                date=self.request.GET.get('date')
                category=self.request.GET.get('category')
                sale_type=self.request.GET.get('sale_type')
                price=self.request.GET.get('price')
                price_per_unit=self.request.GET.get('price_per_unit')
                image=self.request.GET.get('image')
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
        elif self.request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=self.request.user)
            clear.delete()
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
        else:
            pass
        context['search'] = Property.objects.filter(agency=obj.title)
        context['agents'] = Agent.objects.filter(agency=obj.title)
        return context

class AgentDetailView(DetailView):
    model = Agent
    template_name = "agent-page.html"

    def get_object(self, queryset=None):
        global obj
        obj = super(AgentDetailView, self).get_object(queryset=queryset)
        return obj
    def get_context_data(self, **kwargs):
        context = super(AgentDetailView, self).get_context_data(**kwargs)
        if self.request.GET.get('first_check')=="one":
            query = self.request.GET.get('search')
            if query:
                search = Property.filter(Q(address__icontains=query),Q(agency=obj.title))
                context['search'] = search
            else:
                search = self.model.objects.none()
                context['search'] = search
        elif self.request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=self.request.user)
            clear.delete()
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
        else:
            pass
        return context
