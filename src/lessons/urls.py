from django.urls import path

from lessons.views import LessonDetailView

urlpatterns = [
    path("<int:pk>/", LessonDetailView.as_view(), name="lessons"),
]
