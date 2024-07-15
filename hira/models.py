from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# import jsonfield 

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    google_credentials = models.JSONField(null=True, blank=True)
    google_email = models.CharField(max_length=100, null=True, unique=True)

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

    GRADE_CHOICES = [
        ('1', '1st Grade'),
        ('2', '2nd Grade'),
        ('12', '12th Grade'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
    ]
    name = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    languages = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, blank=True)

    

    # Teacher-specific fields
    certifications = models.TextField(blank=True, help_text="List your certifications, separated by commas")
    years_of_experience = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=100, blank=True)
    education = models.TextField(blank=True, help_text="Your educational background")
    teaching_style = models.TextField(blank=True, help_text="Describe your teaching approach")

    # Student-specific fields
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    subjects_of_interest = models.TextField(blank=True, help_text="List subjects you're interested in, separated by commas")
    learning_goals = models.TextField(blank=True, help_text="Describe your learning goals")

    def __str__(self):
        return f'Profile of {self.user.username}'
    
    def get_availability(self):
        return self.availabilities.all().order_by('day', 'start_time')


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username}'



class Availability(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='availabilities')
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name_plural = 'Availabilities'
        unique_together = ['profile', 'day']

    def __str__(self):
        return f"{self.profile.user.username}'s availability on {self.get_day_display()}"
    

class ClassSchedule(models.Model):
    summary = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    attendees = models.ManyToManyField(User, related_name='class_schedules')  
    teacher = models.ForeignKey(User, related_name='class_schedules_as_teacher', on_delete=models.CASCADE)

    def __str__(self):
        return self.summary