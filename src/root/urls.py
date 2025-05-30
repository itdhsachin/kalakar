"""URL configuration for root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from pages.sitemaps import StaticViewSitemap, CourseSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'courses': CourseSitemap,
}

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("courses/", include("courses.urls")),
    path("lessons/", include("lessons.urls")),
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("students/", include("students.urls")),
    path("payment/", include("payment.urls")),
    path("assessment/", include("assessment.urls")),
    path("coupon/", include("coupon.urls")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
