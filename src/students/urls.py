"""URL configuration for the students' app.

This module maps URL patterns to the corresponding views for the students app.

Each route uses the appropriate view and assigns a unique name for URL reversing.
"""

from django.urls import path

from students import views

urlpatterns = [
    path(
        "register/",
        views.StudentRegistrationView.as_view(),
        name="student_registration",
    ),
    path(
        "enroll-course/",
        views.StudentEnrollCourseView.as_view(),
        name="student_enroll_course",
    ),
    path(
        "courses/",
        views.StudentCourseListView.as_view(),
        name="student_course_list",
    ),
    path(
        "coursjes/<pk>/",
        views.StudentCourseDetailView.as_view(),
        name="student_course_detail",
    ),
    path(
        "courses/<pk>/<module_id>",
        views.StudentCourseDetailView.as_view(),
        name="student_course_detail_module",
    ),
]
