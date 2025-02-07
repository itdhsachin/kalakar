from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('thank-you/', views.thankyou, name='thankyou'),

    # Student Competition
    path('competitions/', views.student_competition_list, name='student_competition_list'),
    path('competitions/add/', views.student_competition_add, name='student_competition_add'),
    path('competitions/edit/<int:competition_id>/', views.student_competition_edit, name='student_competition_edit'),
    path('competitions/delete/<int:competition_id>/', views.student_competition_delete, name='student_competition_delete'),

    # Work Submission
    path('assigned-works/', views.assigned_work_list, name='assigned_work_list'),
    path('submit-review/<int:work_id>/', views.submit_review, name='submit_review'),
    path('work/edit/<int:work_id>/', views.edit_work, name='edit_work'),
    path('work/delete/<int:work_id>/', views.delete_work, name='delete_work'),
]
