from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    access_code = models.CharField(max_length=50)

    @property
    def is_teacher(self):
        return self.user_type == 'teacher'

    @property
    def is_student(self):
        return self.user_type == 'student'

User = get_user_model()

class Profile(models.Model):
    LANGUAGE_CHOICES = [
        ('EN', 'English'),
        ('ES', 'Spanish'),
        ('FR', 'French'),
        ('DE', 'German'),
        ('ZH', 'Chinese'),
        # Add more languages as needed
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    languages = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

class TeacherProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='teacherprofile')
    certifications = models.TextField(blank=True, help_text="List your certifications, separated by commas")
    years_of_experience = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=100, blank=True)
    education = models.TextField(blank=True, help_text="Your educational background")
    teaching_style = models.TextField(blank=True, help_text="Describe your teaching approach")

class StudentProfile(models.Model):
    GRADE_CHOICES = [
        ('1', '1st Grade'),
        ('2', '2nd Grade'),
        # ... add more grades as needed
        ('12', '12th Grade'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
    ]

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='studentprofile')
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    subjects_of_interest = models.TextField(blank=True, help_text="List subjects you're interested in, separated by commas")
    learning_goals = models.TextField(blank=True, help_text="Describe your learning goals")