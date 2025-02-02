from django.urls import include, path

from accounts.views import profile

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("profile/", profile, name="profile"),
]
