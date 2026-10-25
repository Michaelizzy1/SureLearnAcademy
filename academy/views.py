from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ContactForm
from .models import Track, BlogPost, Tutor


def home(request):
    return render(request, "academy/home.html", {"active_page": "home"})


def about(request):
    return render(request, "academy/about.html", {"active_page": "about"})


def courses(request):
    tracks = Track.objects.prefetch_related("courses").all()
    return render(request, "academy/courses.html", {"active_page": "courses", "tracks": tracks})


def tutors(request):
    tutor_list = Tutor.objects.all()
    founder = tutor_list.filter(is_founder=True).first()
    return render(request, "academy/tutors.html", {"active_page": "tutors", "founder": founder, "tutors": tutor_list})


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, "academy/blog_list.html", {"active_page": "blog", "posts": posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:3]
    return render(request, "academy/blog_detail.html", {"active_page": "blog", "post": post, "related": related})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks — your enquiry has been sent. We'll be in touch within one business day.")
            return redirect("academy:contact")
    else:
        form = ContactForm()
    return render(request, "academy/contact.html", {"active_page": "contact", "form": form})
