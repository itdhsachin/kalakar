from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.contrib.auth.views import LogoutView

from accounts.views import (
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    dashboard,
    profile,
    update_profile,
    thank_you,
    certificate_view,
    get_districts,
    certificate_detail,
    certificate_list,
    certificate_download

    
    # logout_view
)

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("profile/", profile, name="profile"),
    path("profile/update/", update_profile, name="update_profile"),
    path(
        "password-reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path('accounts/password-reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path(
        "reset_complete/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("dashboard/", dashboard, name="dashboard"),
    path("thank_you/", thank_you, name="thank_you"),
    path("certificate/", certificate_view, name="certificate"),
   
    path("accounts/logout/" , LogoutView.as_view(template_name="accounts/logged_out.html"), name = "logout"),
    path("get-districts/", get_districts, name="get_districts"),
    path('certificates/', certificate_list, name='certificate_list'),
    path('certificate/<int:course_id>/', certificate_detail, name='certificate_detail'),
    path('certificate/<int:course_id>/download/', certificate_download, name='certificate_download'),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
