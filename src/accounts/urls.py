from django.urls import include, path
from django.contrib.auth import views as auth_views
from accounts.views import profile, update_profile,CustomPasswordResetView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("profile/",profile, name="profile"),
    path('profile/update/', update_profile, name='update_profile'),
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset_complete/done/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete")
]
