from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload , name='upload'),
    path('thank-you/', views.thankyou , name='thankyou'),
    path('competitions/', views.student_competition_list, name='student_competition_list'),
    path('competitions/add/', views.student_competition_add, name='student_competition_add'),
    path('competitions/edit/<int:pk>/', views.student_competition_edit, name='student_competition_edit'),
    path('competitions/delete/<int:pk>/', views.student_competition_delete, name='student_competition_delete'),
]