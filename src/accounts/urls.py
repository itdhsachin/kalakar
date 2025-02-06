from django.urls import include, path

from accounts.views import profile, update_profile

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("profile/",profile, name="profile"),
     path('profile/update/', update_profile, name='update_profile'),
]
