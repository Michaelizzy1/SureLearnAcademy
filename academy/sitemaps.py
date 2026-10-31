from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import BlogPost


class StaticViewSitemap(Sitemap):
    protocol = settings.SITEMAP_PROTOCOL
    changefreq = "monthly"

    PRIORITIES = {
        "academy:home": 1.0,
        "academy:courses": 0.9,
        "academy:contact": 0.8,
        "academy:tutors": 0.7,
        "academy:about": 0.7,
        "academy:blog_list": 0.6,
    }

    def items(self):
        return list(self.PRIORITIES)

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.PRIORITIES[item]


class BlogSitemap(Sitemap):
    protocol = settings.SITEMAP_PROTOCOL
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at


sitemaps = {"static": StaticViewSitemap, "blog": BlogSitemap}
