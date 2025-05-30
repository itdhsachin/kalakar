from django.urls import path

from lessons.views import LessonDetailView, track_lesson

urlpatterns = [
    path("<int:pk>/", LessonDetailView.as_view(), name="lessons"),
    path("track_lesson/", track_lesson, name="track_lesson"),
]
