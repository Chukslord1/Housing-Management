from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
app_name = "APP"

urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("index.html", views.IndexListView.as_view(), name="index1"),
    path("login-register.html", views.login_register, name="login_register"),

]
