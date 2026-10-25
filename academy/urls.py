from django.urls import path

from . import views

app_name = "academy"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("courses/", views.courses, name="courses"),
    path("tutors/", views.tutors, name="tutors"),
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("contact/", views.contact, name="contact"),
]
