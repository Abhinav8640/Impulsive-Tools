from django.urls import path
from . import views

app_name = "tools"

urlpatterns = [
    path("", views.home, name="home"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<slug:category_slug>/", views.category_detail, name="category_detail"),
    path("tools/<slug:tool_slug>/", views.tool_detail, name="tool_detail"),
    path("search/", views.search, name="search"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("privacy-policy/", views.privacy, name="privacy"),
    path("terms-conditions/", views.terms, name="terms"),
]
