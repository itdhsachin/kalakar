from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
class AssessmentUpload(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    work = models.BinaryField()  
    filename = models.CharField(max_length=255,default='default_filename.png')  
    content_type = models.CharField(max_length=100,default='application/octet-stream')  

    def __str__(self):
        return f"Submission {self.id} by User {self.user_id.username}"
    
 
class StudentCompetition(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {'Active' if self.status else 'Inactive'}"