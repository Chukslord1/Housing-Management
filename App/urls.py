from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
app_name = "APP"

urlpatterns = [
    path("", views.IndexListView.as_view(), name="index"),
    path("index.html", views.IndexListView.as_view(), name="index1"),
    path("login-register.html", views.login_register, name="login_register"),
    path("logout.html", views.logout, name="logout"),
    path("submit-property.html", views.submit_property, name="submit_property"),
    path("listings-list-full-width.html", views.SearchListView.as_view(), name="advanced_search"),
    path("listings-grid-standard-with-sidebar.html", views.category, name="category"),
    path("listings-list-with-sidebar.html", views.popular, name="popular"),
    path("compare-properties.html", views.compare, name="compare"),
    path("single-property-page-1.html/<slug>", views.PropertyDetailView.as_view(), name="details"),
    path("contact.html", views.contact, name="contact"),
    path("blog.html", views.blog, name="blog"),
]
