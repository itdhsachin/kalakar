# pages/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from courses.models import Course

class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return [
            'pages:index',
            'pages:terms_condition',
            'pages:privacy_policy',
            'pages:faq',
        ]

    def location(self, item):
        return reverse(item)


class CourseSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Course.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
