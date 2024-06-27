from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    access_code = models.CharField(max_length=50)

    def is_teacher(self):
        return self.user_type == 'teacher'

    def is_student(self):
        return self.user_type == 'student'

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
