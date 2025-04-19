from django.db import models

class DailyGoal(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    category=models.CharField(max_length=200, default='General')
    priority=models.CharField(max_length=200,default='Normal')
    is_completed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



# Create your models here.
