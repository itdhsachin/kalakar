from django.db import models
from django.utils import timezone
from django.conf import settings

class AssessmentUpload(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_submissions")  
    work = models.BinaryField()  
    filename = models.CharField(max_length=255, default='default_filename.png')  
    content_type = models.CharField(max_length=100, default='application/octet-stream')  
    assigned_teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_reviews")
    review_score = models.IntegerField(null=True, blank=True)  # Rating 1-5
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for when file is uploaded

    def __str__(self):
        return f"Submission {self.id} by {self.user_id.username} (Teacher: {self.assigned_teacher.username if self.assigned_teacher else 'Not Assigned'})"

class StudentCompetition(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    STATUS_CHOICES = [(1, 'Active'), (0, 'Inactive')]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {'Active' if self.status else 'Inactive'}"
