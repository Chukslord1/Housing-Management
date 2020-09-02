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
from . models import Property,Article,Comparison,UserProfile,Tour,Comment,Agency,Agent,Bookmark,Images,Valuation,Developer,Partner,Boost
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
                compare_count=Comparison.objects.filter(creator=self.request.user).count()
                if compare_count>4:
                    compare_delete=Comparison.objects.filter(creator=self.request.user).latest('date')
                    compare_delete.delete()
                else:
                    pass
        elif self.request.GET.get('third_check')=="three":
            if self.request.user.is_authenticated:
                title=self.request.GET.get('title')
                address=self.request.GET.get('address')
                date=self.request.GET.get('date')
                category=self.request.GET.get('category')
                sale_type=self.request.GET.get('sale_type')
                price=self.request.GET.get('price')
                price_per_unit=self.request.GET.get('price_per_unit')
                image=self.request.GET.get('image')
                print("hello")
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
                book_check=Bookmark.objects.filter(title=title,address=address,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                if book_check:
                    pass
                else:
                    book=Bookmark.objects.create(title=title,address=address,date=date,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                    area=area,rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                    water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                    book.save()

        check_login=self.request.user
        context['houses'] = Property.objects.all()[:6]
        context['articles'] = Article.objects.all()[:3]
        context['lagos'] = Property.objects.filter(Q(address__icontains="lagos")).count()
        context['abuja'] = Property.objects.filter(Q(address__icontains="abuja")).count()
        context['port'] = Property.objects.filter(Q(address__icontains="port")).count()
        context['niger'] = Property.objects.filter(Q(address__icontains="niger")).count()
        context['losangeles'] = Property.objects.filter(Q(address__icontains="losangeles")).count()
        context['sanfransisco'] = Property.objects.filter(Q(address__icontains="sanfransisco")).count()
        context['miami'] = Property.objects.filter(Q(address__icontains="miami")).count()

        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
            context['profile'] = UserProfile.objects.get(user=self.request.user)
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

        paginator= Paginator(Article.objects.all(),10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        if self.request.user.is_authenticated:
            context['profile'] = UserProfile.objects.get(user=self.request.user)

        return context

def login_register(request):
    if request.method == 'POST':
        if request.POST.get("check")=="False":
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("APP:index")
            else:
                context={"message": "invalid login details"}
                return render(request, 'login-register.html')
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
                    context = {'profile':profile,"messages": "User Added"}
                    return render(request,'login-register.html',context)
        else:
            return render(request,'login-register.html')
    return render(request, "login-register.html")


def logout(request):
    auth.logout(request)
    return redirect("index.html")

def submit_property(request):
    profile=''
    if request.user.is_authenticated:
        profile=UserProfile.objects.get(user=request.user)
    context={'profile':profile,"agencies":Agency.objects.all(),"compare":Comparison.objects.all(),"developers":Developer.objects.all()}
    if request.method=="POST":
        title=request.POST.get("title")
        status=request.POST.get("status")
        category=request.POST.get("category")
        price_new=request.POST.get("price")
        developer=request.POST.get("developer")
        if price_new:
            price=int(price_new)
        else:
            price=1000000
        price_per_unit_new=request.POST.get("price_per_unit")
        if price_per_unit_new:
            price_per_unit=int(price_per_unit_new)
        else:
            price_per_unit=2000
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
            rooms=3
        image_1=request.FILES.getlist("image_1")
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
        video=request.FILES.get("video")
        if video:
            video=request.FILES.get("video")
        else:
            video=''
        print(video)
        sewer=request.POST.get("sewer")
        title_new=title.replace(" ","")
        title_final=title_new.replace(":","")
        slug=title_final+status+address+price_new
        property_check=Property.objects.filter(title=title,address=address)
        trial_check=UserProfile.objects.get(user=request.user)
        if request.user.is_authenticated:
            creator=request.user.username
        else:
            creator=""
        if property_check:
            context={'profile':profile,'message':"Property Already Exists","agencies":Agency.objects.all(),"agencies":Agency.objects.all(),"developers":Developer.objects.all(),"compare":Comparison.objects.all()}
        else:
            if trial_check.trials>0 or request.user.is_superuser:
                property=Property.objects.create(title=title,sale_type=status,category=category,price=price,price_per_unit=price_per_unit,agency=agency,
                area=area,rooms=rooms,developer=developer,address=address,
                description=description,building_age=building_age,bedrooms=bedrooms,bathrooms=bathrooms,features=features,parking=parking,cooling=cooling,heating=heating,sewer=sewer,name=name,email=email,phone=phone,slug=slug,creator=creator,video=video)
                property.save()
                for x in image_1:
                    new_image=Images.objects.create(title=title,image=x)
                    new_image.save()
                    property.image_1.add(new_image)
                trial_no=trial_check.trials
                new_trial_value=trial_no-1
                trial_check.trials=new_trial_value
                trial_check.save()
                user_check=User.objects.filter(email=email)
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
                context={'profile':profile,"message":"Successfully Added Property","agencies":Agency.objects.all(),"developers":Developer.objects.all()}
            else:
                context={'profile':profile,"message":"You have exceeded Your Trial of 3 properties submission, please subscribe for a package to continue submitting properties"}
                return redirect("pricing-tables.html")
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
        search=''
        if self.request.GET.get('first_check')=="one":
            first_check="one"
            query = self.request.GET.get('search')
            tab= self.request.GET.get('tab')
            if tab:
                tab= self.request.GET.get('tab')
            else:
                tab="e"
            category= self.request.GET.get('category')
            if category:
                category= self.request.GET.get('category')
            else:
                category="e"
            max_price=self.request.GET.get('max_price')
            if max_price:
                new_max=int(max_price)
            else:
                new_max=10000000000
            if first_check=="one":
                search = self.model.objects.filter(Q(address__icontains=query), Q(sale_type__icontains=tab), Q(category__icontains=category),Q(price__lte=new_max))
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
        elif self.request.GET.get('third_check')=="three":
            if self.request.user.is_authenticated:
                title=self.request.GET.get('title')
                address=self.request.GET.get('address')
                date=self.request.GET.get('date')
                category=self.request.GET.get('category')
                sale_type=self.request.GET.get('sale_type')
                price=self.request.GET.get('price')
                price_per_unit=self.request.GET.get('price_per_unit')
                image=self.request.GET.get('image')
                print("hello")
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
                book_check=Bookmark.objects.filter(title=title,address=address,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                if book_check:
                    pass
                else:
                    book=Bookmark.objects.create(title=title,address=address,date=date,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                    area=area,rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                    water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                    book.save()

        check_login=self.request.user
        context['houses'] = Property.objects.all()[:6]
        context['articles'] = Article.objects.all()[:3]
        context['newyork'] = Property.objects.filter(Q(address__icontains="newYork")).count()
        context['losangeles'] = Property.objects.filter(Q(address__icontains="losangeles")).count()
        context['sanfransisco'] = Property.objects.filter(Q(address__icontains="sanfransisco")).count()
        context['miami'] = Property.objects.filter(Q(address__icontains="miami")).count()
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
            context['profile']=UserProfile.objects.get(user=self.request.user)
        else:
            pass
        if search:
            paginator= Paginator(search,10)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
        return context


class CategoryListView(ListView):
    model = Property
    template_name = "listings-grid-standard-with-sidebar.html"
    def get_context_data(self, **kwargs):
        cat=''
        search=''
        query=''
        context = super(CategoryListView, self).get_context_data(**kwargs)
        if self.request.GET.get('first_check')=="one":
            context['value'] = "Search"
            query = self.request.GET.get('search')
            if query:
                search = self.model.objects.filter(Q(address__icontains=query))
                boost = Boost.objects.all()
                context['search'] = search

            else:
                search = self.model.objects.none()
                context['search'] = search
        elif self.request.GET.get('check_cat')=="True":
            query = self.request.GET.get('cat')
            if query:
                cat = self.model.objects.filter(Q(category__icontains=query))
                context['search'] = cat
                context["cat"]=query
            else:
                cat = self.model.objects.none()
                context['search'] = cat
        elif self.request.GET.get('check_sale')=="True":
            query = self.request.GET.get('sale_type')
            if query:
                cat = self.model.objects.filter(Q(sale_type__icontains=query))
                context['search'] = cat
                context['sale'] = query
            else:
                cat = self.model.objects.none()
                context['search'] = cat
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
        elif self.request.GET.get("filter")=="True":
            filter="True"
            query = self.request.GET.get('search')
            sale_type=self.request.GET.get('sale_type')
            category = self.request.GET.get('category')
            if category:
                category = self.request.GET.get('category')
            else:
                category="e"
            state = self.request.GET.get('state')
            if state:
                state = self.request.GET.get('state')
            else:
                state=query
            if query:
                query= self.request.GET.get('search')
            else:
                query=state
            feature=self.request.GET.get('check')
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
            bedrooms_1 = self.request.GET.get('bedrooms')
            if bedrooms_1:
                bedrooms=int(bedrooms_1)
                bedrooms=bedrooms+1
            else:
                bedrooms=6
            bathrooms_1 = self.request.GET.get('bathrooms')
            if bathrooms_1:
                bathrooms=int(bathrooms_1)
                bathrooms=bathrooms+1
            else:
                bathrooms=6
            if max_price:
                new_max=int(max_price)
            else:
                new_max=10000000000
            if max_area:
                new_max_area=int(max_area)
            else:
                new_max_area=10000000000
            if sale_type:
                sale_type=self.request.GET.get('sale_type')
            else:
                sale_type="e"
            if filter=="True":
                zero=0
                search = self.model.objects.filter(Q(address__icontains=query) | Q(address__icontains=state), Q(sale_type__icontains=sale_type), Q(category__icontains=category),Q(price__lte=new_max),Q(area__lte=new_max_area),Q(bedrooms__lte=bedrooms),Q(bathrooms__lte=bathrooms))
                context['search'] = search
                context['filter'] = "Filter"
            else:
                search = self.model.objects.none()
                context['search'] = search
        elif self.request.GET.get('third_check')=="three":
            if self.request.user.is_authenticated:
                title=self.request.GET.get('title')
                address=self.request.GET.get('address')
                date=self.request.GET.get('date')
                category=self.request.GET.get('category')
                sale_type=self.request.GET.get('sale_type')
                price=self.request.GET.get('price')
                price_per_unit=self.request.GET.get('price_per_unit')
                image=self.request.GET.get('image')
                print("hello")
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
                book_check=Bookmark.objects.filter(title=title,address=address,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                if book_check:
                    pass
                else:
                    book=Bookmark.objects.create(title=title,address=address,date=date,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                    area=area,rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                    water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                    book.save()

        check_login=self.request.user
        context['houses'] = Property.objects.all()[:6]
        context['articles'] = Article.objects.all()[:3]
        if query:
            context['popular'] = Property.objects.filter(Q(category__icontains=query))
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
            context['profile']=UserProfile.objects.get(user=self.request.user)
        else:
            pass
        if cat:
            paginator= Paginator(cat,10)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
        elif search:
            paginator= Paginator(search,10)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
        return context


class PopularListView(ListView):
    model = Property
    template_name = "listings-list-with-sidebar.html"
    def get_context_data(self, **kwargs):
        pop=''
        search=''
        query=''
        context = super(PopularListView, self).get_context_data(**kwargs)
        if self.request.GET.get('first_check')=="one":
            context['value'] = "Search"
            query = self.request.GET.get('search')
            if query:
                search = self.model.objects.filter(Q(address__icontains=query))
                context['search'] = search
            else:
                search = self.model.objects.none()
                context['search'] = search
        elif self.request.GET.get('check_pop')=="True":
            query = self.request.GET.get('pop')
            context['pop']=query
            if query:
                pop = self.model.objects.filter(Q(address__icontains=query))
                context['search'] = pop
            else:
                cat = self.model.objects.none()
                context['search'] = pop
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
        elif self.request.GET.get("filter")=="True":
            context['filter']="Filter"
            filter="True"
            query = self.request.GET.get('search')
            sale_type=self.request.GET.get('sale_type')
            category = self.request.GET.get('category')
            if category:
                category = self.request.GET.get('category')
            else:
                category="e"
            state = self.request.GET.get('state')
            if state:
                state = self.request.GET.get('state')
            else:
                state=query
            if query:
                query= self.request.GET.get('search')
            else:
                query=state
            feature=self.request.GET.get('check')
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
            bedrooms_1 = self.request.GET.get('bedrooms')
            if bedrooms_1:
                bedrooms=int(bedrooms_1)
                bedrooms=bedrooms+1
            else:
                bedrooms=6
            bathrooms_1 = self.request.GET.get('bathrooms')
            if bathrooms_1:
                bathrooms=int(bathrooms_1)
                bathrooms=bathrooms+1
            else:
                bathrooms=6
            if max_price:
                new_max=int(max_price)
            else:
                new_max=10000000000
            if max_area:
                new_max_area=int(max_area)
            else:
                new_max_area=10000000000
            if sale_type:
                sale_type=self.request.GET.get('sale_type')
            else:
                sale_type="e"
            if filter=="True":
                zero=0
                search = self.model.objects.filter(Q(address__icontains=query) | Q(address__icontains=state), Q(sale_type__icontains=sale_type), Q(category__icontains=category),Q(price__lte=new_max),Q(area__lte=new_max_area),Q(bedrooms__lte=bedrooms),Q(bathrooms__lte=bathrooms))
                context['search'] = search
            else:
                search = self.model.objects.none()
                context['search'] = search
        elif self.request.GET.get('third_check')=="three":
            if self.request.user.is_authenticated:
                title=self.request.GET.get('title')
                address=self.request.GET.get('address')
                date=self.request.GET.get('date')
                category=self.request.GET.get('category')
                sale_type=self.request.GET.get('sale_type')
                price=self.request.GET.get('price')
                price_per_unit=self.request.GET.get('price_per_unit')
                image=self.request.GET.get('image')
                print("hello")
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
                book_check=Bookmark.objects.filter(title=title,address=address,category=category,sale_type=sale_type,image_1=image_url,
                rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                if book_check:
                    pass
                else:
                    book=Bookmark.objects.create(title=title,address=address,date=date,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                    area=area,rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                    water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                    book.save()

        check_login=self.request.user
        context['houses'] = Property.objects.all()[:6]
        context['articles'] = Article.objects.all()[:3]
        context['popular'] = Property.objects.filter(Q(address__icontains=query))
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
            context['profile']=UserProfile.objects.get(user=self.request.user)
        else:
            pass
        if pop:
            paginator= Paginator(Property.objects.filter(address__icontains=query),10)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
        elif search:
            paginator= Paginator(search,10)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
        return context


def compare(request):
    profile=''
    if request.user.is_authenticated:
        profile=UserProfile.objects.get(user=request.user)
    compare=Comparison.objects.all()
    context={"compare":compare,'profile':profile}
    if request.GET.get('clear')=="True":
        clear=Comparison.objects.filter(creator=request.user)
        clear.delete()
        return redirect("compare-properties.html")
    return render(request,"compare-properties.html",context)

def contact(request):
    profile=''
    if request.user.is_authenticated:
        profile=UserProfile.objects.get(user=request.user)
    context={"compare":Comparison.objects.all,'profile':profile}
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
        context={'profile':profile,'message':'Your message has been sent sucessfully',"compare":Comparison.objects.all()}
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
                property=obj.title
                email= self.request.user.email
                message="Request for inspection of "+property +" on the "+ date+ " by " + time
                fromaddr = "housing-send@advancescholar.com"
                toaddr = "admin@afriproperty.com.ng"
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] ="Enquiry For Property"


                body = message+ "my contacts are"  + " email " + email
                msg.attach(MIMEText(body, 'plain'))

                server = smtplib.SMTP('mail.advancescholar.com',  26)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login("housing-send@advancescholar.com", "housing@24hubs.com")
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                context['message']="Inspection Request Saved Successfully"
            else:
                tour=Tour.objects.create(date=date,time=time,property=obj.title,phone=phone,name=name)
                tour.save()
                property=obj.title
                message="Request for inspection of "+property +" on the "+ date+ " by " + time
                fromaddr = "housing-send@advancescholar.com"
                toaddr = "admin@afriproperty.com.ng"
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] ="Enquiry For Property"


                body = message+ "my contacts are"  + " phone " + phone
                msg.attach(MIMEText(body, 'plain'))

                server = smtplib.SMTP('mail.advancescholar.com',  26)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login("housing-send@advancescholar.com", "housing@24hubs.com")
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                context['message']="Inspection Request Saved Successfully"
        elif self.request.GET.get("send")=="True":
            email=self.request.GET.get('email')
            message=self.request.GET.get('message')
            fromaddr = "housing-send@advancescholar.com"
            toaddr = self.request.GET.get('to')
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] ="Enquiry For Property"


            body = message+ "my contacts are"  + " email " + email
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('mail.advancescholar.com',  26)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("housing-send@advancescholar.com", "housing@24hubs.com")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            context['message']="Sent Enquiry Successfully"
        elif self.request.GET.get("report")=="True":
            title=self.request.GET.get("title")
            fromaddr = "housing-send@advancescholar.com"
            toaddr = "admin@afriproperty.com.ng"
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] ="Report Listing"


            body = "A listing was reported, A Property Listing with the name :" + title
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('mail.advancescholar.com',  26)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("housing-send@advancescholar.com", "housing@24hubs.com")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            context['message']="Reported Successfully"
        check_login=self.request.user
        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
            context['profile']=UserProfile.objects.get(user=self.request.user)
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
            context['profile']=UserProfile.objects.get(user=self.request.user)
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
        if self.request.user.is_authenticated:
            context["compare"] = Comparison.objects.all()
            context['profile']=UserProfile.objects.get(user=self.request.user)
        paginator= Paginator(Agency.objects.all(),10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

class DeveloperListView(ListView):
    model = Developer
    template_name = "developer-list.html"
    def get_context_data(self, **kwargs):
        context = super(DeveloperListView, self).get_context_data(**kwargs)
        if self.request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=self.request.user)
            clear.delete()
        if self.request.user.is_authenticated:
            context["compare"] = Comparison.objects.all()
            context['profile']=UserProfile.objects.get(user=self.request.user)
        paginator= Paginator(Agency.objects.all(),10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class PartnerListView(ListView):
    model = Partner
    template_name = "partners.html"
    def get_context_data(self, **kwargs):
        context = super(PartnerListView, self).get_context_data(**kwargs)
        if self.request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=self.request.user)
            clear.delete()
        if self.request.user.is_authenticated:
            context["compare"] = Comparison.objects.all()
            context['profile']=UserProfile.objects.get(user=self.request.user)
        paginator= Paginator(Partner.objects.all(),10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
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
        elif self.request.GET.get("send")=="True":
            email=self.request.GET.get('email')
            message=self.request.GET.get('message')
            fromaddr = "housing-send@advancescholar.com"
            toaddr = self.request.GET.get('to')
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] ="Assistance For Property"


            body = message+ "my contacts are"  + " email " + email
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('mail.advancescholar.com',  26)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("housing-send@advancescholar.com", "housing@24hubs.com")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            context['message']="Sent Enquiry Successfully"
        elif self.request.GET.get('third_check')=="three":
            if self.request.user.is_authenticated:
                title=self.request.GET.get('title')
                address=self.request.GET.get('address')
                date=self.request.GET.get('date')
                category=self.request.GET.get('category')
                sale_type=self.request.GET.get('sale_type')
                price=self.request.GET.get('price')
                price_per_unit=self.request.GET.get('price_per_unit')
                image=self.request.GET.get('image')
                print("hello")
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
                book_check=Bookmark.objects.filter(title=title,address=address,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                if book_check:
                    pass
                else:
                    book=Bookmark.objects.create(title=title,address=address,date=date,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                    area=area,rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                    water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                    book.save()

        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
            context['profile']=UserProfile.objects.get(user=self.request.user)
        else:
            pass

        context['search'] = Property.objects.filter(agency=obj.title)
        context['agents'] = Agent.objects.filter(agency=obj.title)
        paginator= Paginator(Agency.objects.all(),10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

class DeveloperDetailView(DetailView):
    model = Developer
    template_name = "developer-page.html"

    def get_object(self, queryset=None):
        global obj
        obj = super(DeveloperDetailView, self).get_object(queryset=queryset)
        return obj
    def get_context_data(self, **kwargs):
        context = super(DeveloperDetailView, self).get_context_data(**kwargs)
        if self.request.GET.get('first_check')=="one":
            query = self.request.GET.get('search')
            if query:
                search = Property.filter(Q(address__icontains=query),Q(developer=obj.title))
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
        elif self.request.GET.get("send")=="True":
            email=self.request.GET.get('email')
            message=self.request.GET.get('message')
            fromaddr = "housing-send@advancescholar.com"
            toaddr = self.request.GET.get('to')
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] ="Assistance For Property"


            body = message+ "my contacts are"  + " email " + email
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('mail.advancescholar.com',  26)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("housing-send@advancescholar.com", "housing@24hubs.com")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            context['message']="Sent Enquiry Successfully"
        elif self.request.GET.get('third_check')=="three":
            if self.request.user.is_authenticated:
                title=self.request.GET.get('title')
                address=self.request.GET.get('address')
                date=self.request.GET.get('date')
                category=self.request.GET.get('category')
                sale_type=self.request.GET.get('sale_type')
                price=self.request.GET.get('price')
                price_per_unit=self.request.GET.get('price_per_unit')
                image=self.request.GET.get('image')
                print("hello")
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
                book_check=Bookmark.objects.filter(title=title,address=address,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                if book_check:
                    pass
                else:
                    book=Bookmark.objects.create(title=title,address=address,date=date,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                    area=area,rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                    water=water,exercise_room=exercise_room,storage_room=storage_room,creator=self.request.user)
                    book.save()

        if self.request.user.is_authenticated:
            context['compare'] = Comparison.objects.filter(creator=self.request.user)
            context['profile']=UserProfile.objects.get(user=self.request.user)
        else:
            pass

        context['search'] = Property.objects.filter(developer=obj.title)
        context['agents'] = Agent.objects.filter(agency=obj.title)
        paginator= Paginator(Developer.objects.all(),10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
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
            context['profile']=UserProfile.objects.get(user=self.request.user)
        else:
            pass
        return context

def profile(request):
    profile=''
    if request.user.is_authenticated:
        profile=UserProfile.objects.get(user=request.user)
    context={"profile":profile}
    if request.method=="POST":
        name=request.POST.get("name")
        title=request.POST.get("title")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        about=request.POST.get("about")
        twitter=request.POST.get("twitter")
        facebook=request.POST.get("facebook")
        google=request.POST.get("google")
        linkedin=request.POST.get("linkedin")
        image=request.FILES.get("image")
        data=UserProfile.objects.get(user=request.user)
        if name:
            data.name=name
        if title:
            data.title=title
        if phone:
            data.phone=phone
        if email:
            data.email=email
        if about:
            data.about=about
        if twitter:
            data.twitter=twitter
        if facebook:
            data.facebook=facebook
        if google:
            data.googl=google
        if linkedin:
            data.linkedin=linkedin
        if image:
            data.image=image
        data.save()
    return render(request,"my-profile.html",context)

def properties(request):
    profile=''
    if request.user.is_authenticated:
        profile=UserProfile.objects.get(user=request.user)
    context={"compare":Comparison.objects.all(),"properties":Property.objects.filter(creator=request.user),"profile":profile}
    if request.method=="POST":
        if request.POST.get("delete")=="True":
            title=request.POST.get("title")
            data=Property.objects.filter(title=title)
            data.delete()
        elif request.POST.get("boost")=="True":
            title=request.POST.get("title")
            image=request.POST.get("image")
            image_url=image.replace('/media/','')
            data=Boost.objects.create(title=title,image=image_url)
            data.save
    elif request.method=="GET":
        if request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=request.user)
            clear.delete()
    return render(request,"my-properties.html",context)

def password(request):
    context={"compare":Comparison.objects.filter(creator=request.user),"profile":UserProfile.objects.get(user=request.user)}
    if request.method=="POST":
        current=request.POST.get("current")
        password=request.POST.get("password")
        confirm=request.POST.get('confirm')
        print(current)
        if auth.authenticate(username=request.user, password=current):
            if password==confirm:
                data=User.objects.get(username=request.user)
                print(data)
                data.set_password(password)
                data.save()
                return redirect("index.html")
    elif request.method=="GET":
        if request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=request.user)
            clear.delete()
    return render(request,"change-password.html",context)

def bookmark(request):
    context={"compare":Comparison.objects.filter(creator=request.user),"books":Bookmark.objects.filter(creator=request.user),"profile":UserProfile.objects.get(user=request.user)}
    if request.method=="POST":
        if request.POST.get("delete")=="True":
            title=request.POST.get("title")
            data=Bookmark.objects.filter(title=title)
            data.delete()
    elif request.method=="GET":
        if request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=request.user)
            clear.delete()
    return render(request,"my-bookmarks.html",context)

def agents(request):
    context={}
    profile=''
    paginator= Paginator(Agent.objects.all(),10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        context={"compare":Comparison.objects.filter(creator=request.user),"profile":profile,"agents":Agent.objects.all(),"page_obj":page_obj}
    if request.method=="GET":
        if request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=request.user)
            clear.delete()
        elif request.GET.get("check")=="True":
            query = request.GET.get('search')
            if query:
                search = Agent.objects.filter(Q(address__icontains=query) | Q(name__icontains=query))
                context['search'] = search

            else:
                search = Agent.objects.none()
                context['search'] = search

    return render(request,"agents-list.html",context)

def pricing(request):
    if request.method=="POST":
        if request.POST.get("paid")=="True" and request.POST.get("amount")=="3000":
            trial_check=UserProfile.objects.get(user=request.user)
            trial_no=trial_check.trials
            new_trial_value=trial_no+20
            trial_check.trials=new_trial_value
            trial_check.save()
        elif request.POST.get("paid")=="True" and request.POST.get("amount")=="10000":
            trial_check=UserProfile.objects.get(user=request.user)
            trial_no=trial_check.trials
            new_trial_value=trial_no+100
            trial_check.trials=new_trial_value
            trial_check.save()
        else:
            pass
    return render(request,"pricing-tables.html")


def property_video(request):
    pop=''
    search=''
    query=''
    context = {}
    if request.GET.get('first_check')=="one":
        query = request.GET.get('search')
        if query:
            search = Property.objects.filter(Q(address__icontains=query))
            paginator= Paginator(search,10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context= {"search":search,'page_obj':page_obj}
        else:
            search = Property.objects.none()
            context= {"search":search}
    elif request.GET.get('check_pop')=="True":
        query = request.GET.get('pop')
        context['pop']=query
        if query:
            pop = Property.objects.filter(Q(address__icontains=query))
            paginator= Paginator(pop,10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context= {"search":pop,'page_obj':page_obj}
        else:
            cat = Property.objects.none()
            context= {"search":pop}
    elif request.GET.get('clear')=="True":
        clear=Comparison.objects.filter(creator=request.user)
        clear.delete()
    elif request.GET.get('second_check')=="two":
        if request.user.is_authenticated:
            title=request.GET.get('title')
            address=request.GET.get('address')
            date=request.GET.get('date')
            category=request.GET.get('category')
            sale_type=request.GET.get('sale_type')
            price=request.GET.get('price')
            price_per_unit=request.GET.get('price_per_unit')
            image=request.GET.get('image')
            image_url=image.replace('/media/','')
            area=request.GET.get('area')
            rooms=request.GET.get('rooms')
            bedrooms=request.GET.get('bedrooms')
            bathrooms=request.GET.get('bathrooms')
            features=request.GET.get('features')
            building_age=request.GET.get('building_age')
            parking=request.GET.get('parking')
            cooling=request.GET.get('cooling')
            heating=request.GET.get('heating')
            sewer=request.GET.get('sewer')
            water=request.GET.get('water')
            exercise_room=request.GET.get('exercise_room')
            storage_room=request.GET.get('storage_room')
            compare_check=Comparison.objects.filter(title=title,address=address,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
            rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
            water=water,exercise_room=exercise_room,storage_room=storage_room,creator=request.user)
            if compare_check:
                pass
            else:
                compare=Comparison.objects.create(title=title,address=address,date=date,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                area=area,rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                water=water,exercise_room=exercise_room,storage_room=storage_room,creator=request.user)
                compare.save()
            compare_count=Comparison.objects.filter(creator=request.user).count()
            if compare_count>3:
                compare_delete=Comparsion.objects.filter(creator=request.user)[4:]
                compare_delete.delete()
            else:
                pass
    elif request.GET.get("filter")=="True":
        filter="True"
        query = request.GET.get('search')
        sale_type=request.GET.get('sale_type')
        category = request.GET.get('category')
        if category:
            category = request.GET.get('category')
        else:
            category="e"
        state = request.GET.get('state')
        if state:
            state = request.GET.get('state')
        else:
            state=query
        if query:
            query= request.GET.get('search')
        else:
            query=state
        feature=request.GET.get('check')
        min_area_1 = request.GET.get('min_area_1')
        max_area_1 = request.GET.get('max_area_1')
        min_price_1 = request.GET.get('min_price_1')
        max_price_1 = request.GET.get('max_price_1')
        min_area_2=min_area_1.replace("+","")
        max_area_2=max_area_1.replace("+","")
        min_price_2=min_price_1.replace("+","")
        max_price_2=max_price_1.replace("+","")
        min_area=min_area_1.replace(" ","")
        max_area=max_area_1.replace(" ","")
        min_price=min_price_1.replace(" ","")
        max_price=max_price_1.replace(" ","")
        bedrooms_1 = request.GET.get('bedrooms')
        if bedrooms_1:
            bedrooms=int(bedrooms_1)
            bedrooms=bedrooms+1
        else:
            bedrooms=6
        bathrooms_1 = request.GET.get('bathrooms')
        if bathrooms_1:
            bathrooms=int(bathrooms_1)
            bathrooms=bathrooms+1
        else:
            bathrooms=6
        if max_price:
            new_max=int(max_price)
        else:
            new_max=10000000000
        if max_area:
            new_max_area=int(max_area)
        else:
            new_max_area=10000000000
        if sale_type:
            sale_type=request.GET.get('sale_type')
        else:
            sale_type="e"
        if filter=="True":
            zero=0
            search = Property.objects.filter(Q(address__icontains=query) | Q(address__icontains=state), Q(sale_type__icontains=sale_type), Q(category__icontains=category),Q(price__lte=new_max),Q(area__lte=new_max_area),Q(bedrooms__lte=bedrooms),Q(bathrooms__lte=bathrooms))
            paginator= Paginator(search,10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context={"search":search,"page_obj":page_obj}
        else:
            search = Property.objects.none()
            context={"search":search}
    elif request.GET.get('third_check')=="three":
        if request.user.is_authenticated:
            title=request.GET.get('title')
            address=request.GET.get('address')
            date=request.GET.get('date')
            category=request.GET.get('category')
            sale_type=request.GET.get('sale_type')
            price=request.GET.get('price')
            price_per_unit=request.GET.get('price_per_unit')
            image=request.GET.get('image')
            image_url=image.replace('/media/','')
            area=request.GET.get('area')
            rooms=request.GET.get('rooms')
            bedrooms=request.GET.get('bedrooms')
            bathrooms=request.GET.get('bathrooms')
            features=request.GET.get('features')
            building_age=request.GET.get('building_age')
            parking=request.GET.get('parking')
            cooling=request.GET.get('cooling')
            heating=request.GET.get('heating')
            sewer=request.GET.get('sewer')
            water=request.GET.get('water')
            exercise_room=request.GET.get('exercise_room')
            storage_room=request.GET.get('storage_room')
            book_check=Bookmark.objects.filter(title=title,address=address,category=category,sale_type=sale_type,image_1=image_url,
            rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
            water=water,exercise_room=exercise_room,storage_room=storage_room,creator=request.user)
            if book_check:
                pass
            else:
                book=Bookmark.objects.create(title=title,address=address,date=date,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                area=area,rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                water=water,exercise_room=exercise_room,storage_room=storage_room,creator=request.user)
                book.save()

    else:
        if request.user.is_authenticated:
            pop=Property.objects.filter(Q(address__icontains=query))
            paginator= Paginator(pop,10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context={"compare":Comparison.objects.filter(creator=request.user),'popular':pop,'profile':UserProfile.objects.get(user=request.user),"page_obj":page_obj}
        else:
            pop=Property.objects.filter(Q(address__icontains=query))
            paginator= Paginator(pop,10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context={'popular':Property.objects.filter(Q(address__icontains=query)),"page_obj":page_obj}
    return render(request,"property-video.html",context)



def property_valuation(request):
    profile=''
    if request.user.is_authenticated:
        profile=UserProfile.objects.get(user=request.user)
    context={'profile':profile,"agencies":Agency.objects.all(),"compare":Comparison.objects.all()}
    if request.method=="POST":
        status=request.POST.get("status")
        category=request.POST.get("category")
        price=request.POST.get("price")
        area=request.POST.get("area")
        rooms=request.POST.get("rooms")
        address=request.POST.get("address")
        bedrooms=request.POST.get("bedrooms")
        building_age=request.POST.get("building_age")
        bathrooms=request.POST.get("bathrooms")
        features=request.POST.get("features")
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        parking=request.POST.get("parking")
        cooling=request.POST.get("cooling")
        heating=request.POST.get("heating")
        sewer=request.POST.get("sewer")
        image=request.FILES.get("image")

        fromaddr = "housing-send@advancescholar.com"
        toaddr = "admin@afripropert.com.ng"
        subject="Property Request"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "A request for a Property Valuation"

        test=Valuation.objects.create(image=image,sale_type=status,category=category,price=price,area=area,rooms=rooms,address=address,bedrooms=bedrooms,building_age=building_age,bathrooms=bathrooms,
        features=features,user=name,email=email,phone=phone,parking=parking,cooling=cooling,heating=heating,sewer=sewer)
        test.save()
        body = "A request for a property valuation has been sent from "+name+" email is  "+ email + ".  Requirements are:"+" A "+category+ " property for " + status + ","+ " with a price of "+price+" with an area of "+area+" per sq m "+","+rooms+" rooms "+" at a location: "+address+" with "+bedrooms+" bedrooms "+building_age+" years building age "+bathrooms+" bathrooms. "+" extra features: "+features+","+parking+" parking,"+cooling+' cooling,'+heating+' heating,'+sewer+' sewage.'
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('mail.advancescholar.com',  26)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("housing-send@advancescholar.com", "housing@24hubs.com")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        context={'profile':profile,"message":"Successfully Submitted  Request"}
    elif request.method=="GET":
        if request.GET.get('clear')=="True":
            clear=Comparison.objects.filter(creator=request.user)
            clear.delete()
    return render(request,"property-valuation.html",context)


def multi_component(request):
    pop=''
    search=''
    query=''
    context = {}
    if request.GET.get('first_check')=="one":
        query = request.GET.get('search')
        if query:
            search = Property.objects.filter(Q(address__icontains=query))
            paginator= Paginator(search,10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context= {"search":search,'page_obj':page_obj}
        else:
            search = Property.objects.none()
            context= {"search":search}
    elif request.GET.get('check_pop')=="True":
        query = request.GET.get('pop')
        context['pop']=query
        if query:
            pop = Property.objects.filter(Q(address__icontains=query))
            paginator= Paginator(pop,10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context= {"search":pop,'page_obj':page_obj}
        else:
            cat = Property.objects.none()
            context= {"search":pop}
    elif request.GET.get('clear')=="True":
        clear=Comparison.objects.filter(creator=request.user)
        clear.delete()
    elif request.GET.get('second_check')=="two":
        if request.user.is_authenticated:
            title=request.GET.get('title')
            address=request.GET.get('address')
            date=request.GET.get('date')
            category=request.GET.get('category')
            sale_type=request.GET.get('sale_type')
            price=request.GET.get('price')
            price_per_unit=request.GET.get('price_per_unit')
            image=request.GET.get('image')
            image_url=image.replace('/media/','')
            area=request.GET.get('area')
            rooms=request.GET.get('rooms')
            bedrooms=request.GET.get('bedrooms')
            bathrooms=request.GET.get('bathrooms')
            features=request.GET.get('features')
            building_age=request.GET.get('building_age')
            parking=request.GET.get('parking')
            cooling=request.GET.get('cooling')
            heating=request.GET.get('heating')
            sewer=request.GET.get('sewer')
            water=request.GET.get('water')
            exercise_room=request.GET.get('exercise_room')
            storage_room=request.GET.get('storage_room')
            compare_check=Comparison.objects.filter(title=title,address=address,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
            rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
            water=water,exercise_room=exercise_room,storage_room=storage_room,creator=request.user)
            if compare_check:
                pass
            else:
                compare=Comparison.objects.create(title=title,address=address,date=date,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                area=area,rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                water=water,exercise_room=exercise_room,storage_room=storage_room,creator=request.user)
                compare.save()
            compare_count=Comparison.objects.filter(creator=request.user).count()
            if compare_count>3:
                compare_delete=Comparsion.objects.filter(creator=request.user)[4:]
                compare_delete.delete()
            else:
                pass
    elif request.GET.get("filter")=="True":
        filter="True"
        query = request.GET.get('search')
        sale_type=request.GET.get('sale_type')
        category = request.GET.get('category')
        if category:
            category = request.GET.get('category')
        else:
            category="e"
        state = request.GET.get('state')
        if state:
            state = request.GET.get('state')
        else:
            state=query
        if query:
            query= request.GET.get('search')
        else:
            query=state
        feature=request.GET.get('check')
        min_area_1 = request.GET.get('min_area_1')
        max_area_1 = request.GET.get('max_area_1')
        min_price_1 = request.GET.get('min_price_1')
        max_price_1 = request.GET.get('max_price_1')
        min_area_2=min_area_1.replace("+","")
        max_area_2=max_area_1.replace("+","")
        min_price_2=min_price_1.replace("+","")
        max_price_2=max_price_1.replace("+","")
        min_area=min_area_1.replace(" ","")
        max_area=max_area_1.replace(" ","")
        min_price=min_price_1.replace(" ","")
        max_price=max_price_1.replace(" ","")
        bedrooms_1 = request.GET.get('bedrooms')
        if bedrooms_1:
            bedrooms=int(bedrooms_1)
            bedrooms=bedrooms+1
        else:
            bedrooms=6
        bathrooms_1 = request.GET.get('bathrooms')
        if bathrooms_1:
            bathrooms=int(bathrooms_1)
            bathrooms=bathrooms+1
        else:
            bathrooms=6
        if max_price:
            new_max=int(max_price)
        else:
            new_max=10000000000
        if max_area:
            new_max_area=int(max_area)
        else:
            new_max_area=10000000000
        if sale_type:
            sale_type=request.GET.get('sale_type')
        else:
            sale_type="e"
        if filter=="True":
            zero=0
            search = Property.objects.filter(Q(address__icontains=query) | Q(address__icontains=state), Q(sale_type__icontains=sale_type), Q(category__icontains=category),Q(price__lte=new_max),Q(area__lte=new_max_area),Q(bedrooms__lte=bedrooms),Q(bathrooms__lte=bathrooms))
            paginator= Paginator(search,10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context={"search":search,"page_obj":page_obj}
        else:
            search = Property.objects.none()
            context={"search":search}
    elif request.GET.get('third_check')=="three":
        if request.user.is_authenticated:
            title=request.GET.get('title')
            address=request.GET.get('address')
            date=request.GET.get('date')
            category=request.GET.get('category')
            sale_type=request.GET.get('sale_type')
            price=request.GET.get('price')
            price_per_unit=request.GET.get('price_per_unit')
            image=request.GET.get('image')
            image_url=image.replace('/media/','')
            area=request.GET.get('area')
            rooms=request.GET.get('rooms')
            bedrooms=request.GET.get('bedrooms')
            bathrooms=request.GET.get('bathrooms')
            features=request.GET.get('features')
            building_age=request.GET.get('building_age')
            parking=request.GET.get('parking')
            cooling=request.GET.get('cooling')
            heating=request.GET.get('heating')
            sewer=request.GET.get('sewer')
            water=request.GET.get('water')
            exercise_room=request.GET.get('exercise_room')
            storage_room=request.GET.get('storage_room')
            book_check=Bookmark.objects.filter(title=title,address=address,category=category,sale_type=sale_type,image_1=image_url,
            rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
            water=water,exercise_room=exercise_room,storage_room=storage_room,creator=request.user)
            if book_check:
                pass
            else:
                book=Bookmark.objects.create(title=title,address=address,date=date,category=category,sale_type=sale_type,price=price,price_per_unit=price_per_unit,image_1=image_url,
                area=area,rooms=rooms,bedrooms=bedrooms,bathrooms=bathrooms,features=features,building_age=building_age,parking=parking,cooling=cooling,heating=heating,sewer=sewer,
                water=water,exercise_room=exercise_room,storage_room=storage_room,creator=request.user)
                book.save()

    else:
        if request.user.is_authenticated:
            pop=Property.objects.filter(Q(address__icontains=query))
            paginator= Paginator(pop,10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context={"compare":Comparison.objects.filter(creator=request.user),'popular':pop,'profile':UserProfile.objects.get(user=request.user),"page_obj":page_obj}
        else:
            pop=Property.objects.filter(Q(address__icontains=query))
            paginator= Paginator(pop,10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context={'popular':Property.objects.filter(Q(address__icontains=query)),"page_obj":page_obj}
    return render(request,"multilevel-component.html",context)
