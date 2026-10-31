from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ContactForm
from .models import Track, BlogPost, Tutor
from .seo import (absolute, breadcrumb_schema, faq_schema, ld_json,
                  organization_schema, website_schema)

def meta(title, description, image=None, og_type="website", noindex=False):
    return {
        "seo_title": title,
        "seo_description": description,
        "seo_image": image,
        "seo_og_type": og_type,
        "seo_noindex": noindex,
    }


HOME_FAQ = [
    ("Are lessons only available at home?",
     "No, you can choose home visits, online lessons, or a mix of both depending on what works for you."),
    ("How are tutors selected?",
     "Tutors are matched to each learner based on subject expertise and the student's current level and pace."),
    ("Can I try a lesson before committing?",
     "Yes, every enquiry starts with a free consultation so we can understand your goals before any commitment."),
    ("Do you teach both exam prep and tech skills to the same student?",
     "Absolutely. Some learners take both, for example JAMB prep alongside web development."),
]


def home(request):
    schema = ld_json(organization_schema(), website_schema(), faq_schema(HOME_FAQ))
    return render(request, "academy/home.html", {"active_page": "home", "schema_json": schema, **meta("Private & Home Lessons in Abuja | SureLearn Academy", "One-on-one private and home lessons in Abuja and Nasarawa: SSCE & JAMB prep, web development, programming, AI and design. Book a free consultation.")})


def about(request):
    schema = ld_json(breadcrumb_schema(("Home", "/"), ("About Us", "/about/")))
    return render(request, "academy/about.html", {"active_page": "about", "schema_json": schema, **meta("About Us | Private Tutors in Abuja | SureLearn Academy", "Meet SureLearn Academy: how we match learners in Abuja and Nasarawa with vetted tutors for one-on-one home and online lessons built around each student.")})


def courses(request):
    tracks = Track.objects.prefetch_related("courses").all()
    courses_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "SureLearn Academy courses",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i,
                "item": {
                    "@type": "Course",
                    "name": c.title,
                    "description": c.description,
                    "provider": {"@type": "Organization", "name": "SureLearn Academy", "sameAs": absolute("/")},
                },
            }
            for i, c in enumerate((c for t in tracks for c in t.courses.all()), start=1)
        ],
    }
    schema = ld_json(breadcrumb_schema(("Home", "/"), ("Courses", "/courses/")), courses_ld)
    return render(request, "academy/courses.html", {"active_page": "courses", "tracks": tracks, "schema_json": schema, **meta("SSCE, JAMB, Coding & Design Courses in Abuja | SureLearn", "Browse SureLearn Academy courses: SSCE and JAMB prep, web development, programming, AI, graphics design and UI/UX, taught one-on-one at home or online.")})


def tutors(request):
    tutor_list = Tutor.objects.all()
    founder = tutor_list.filter(is_founder=True).first()
    schema = ld_json(breadcrumb_schema(("Home", "/"), ("Our Tutors", "/tutors/")))
    return render(request, "academy/tutors.html", {"active_page": "tutors", "founder": founder, "tutors": tutor_list, "schema_json": schema, **meta("Our Tutors | Home & Online Tutors in Abuja | SureLearn", "Meet the vetted tutors behind SureLearn Academy: experienced in SSCE, JAMB, web development, programming and creative skills, teaching at home or online.")})


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    schema = ld_json(breadcrumb_schema(("Home", "/"), ("Blog", "/blog/")))
    return render(request, "academy/blog_list.html", {"active_page": "blog", "posts": posts, "schema_json": schema, **meta("Study Tips & Exam Guidance Blog | SureLearn Academy", "Practical study tips, JAMB and SSCE exam guidance, and tutor insights from SureLearn Academy to help Nigerian students learn smarter.")})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related = BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:3]
    article = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": post.excerpt,
        "datePublished": post.published_at.isoformat(),
        "dateModified": post.published_at.isoformat(),
        "author": {"@type": "Organization", "name": post.author_name},
        "publisher": {"@id": absolute("/#organization")},
        "mainEntityOfPage": absolute(post.get_absolute_url()),
        "inLanguage": "en-NG",
    }
    if post.cover_image:
        article["image"] = absolute(post.cover_image.url)
    schema = ld_json(
        article,
        breadcrumb_schema(("Home", "/"), ("Blog", "/blog/"), (post.title, post.get_absolute_url())),
    )
    return render(request, "academy/blog_detail.html", {
        "active_page": "blog", "post": post, "related": related, "schema_json": schema,
        **meta(
            f"{post.title} | SureLearn Academy Blog",
            (post.excerpt[:157] + "...") if len(post.excerpt) > 160 else post.excerpt,
            image=absolute(post.cover_image.url) if post.cover_image else None,
            og_type="article",
        ),
    })


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks — your enquiry has been sent. We'll be in touch within one business day.")
            return redirect("academy:contact")
    else:
        form = ContactForm()
    schema = ld_json(breadcrumb_schema(("Home", "/"), ("Contact Us", "/contact/")))
    return render(request, "academy/contact.html", {"active_page": "contact", "form": form, "schema_json": schema, **meta("Book a Free Consultation | SureLearn Academy Abuja", "Tell us what you want to learn and we will match you with the right tutor in Abuja, Nasarawa or online. Free consultation, reply within one business day.")})
