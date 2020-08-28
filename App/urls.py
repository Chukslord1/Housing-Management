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
    path("listing.html", views.SearchListView.as_view(), name="advanced_search"),
    path("category", views.CategoryListView.as_view(), name="category"),
    path("popular", views.PopularListView.as_view(), name="popular"),
    path("compare-properties.html", views.compare, name="compare"),
    path("single-property-page-1.html/<slug>", views.PropertyDetailView.as_view(), name="details"),
    path("contact.html", views.contact, name="contact"),
    path("my-profile.html", views.profile, name="profile"),
    path("my-bookmarks.html", views.bookmark, name="bookmarks"),
    path("my-properties.html", views.properties, name="properties"),
    path("change-password.html", views.password, name="password"),
    path("blog-post.html/<slug>", views.ArticleDetailView.as_view(), name="blog"),
    path("blog.html", views.ArticleListView.as_view(), name="blog-list"),
    path("agencies-list.html", views.AgencyListView.as_view(), name="agencies-list"),
    path("agency-page.html/<slug>", views.AgencyDetailView.as_view(), name="agencies"),
    path("agent-page.html/<slug>", views.AgentDetailView.as_view(), name="agents"),
]
