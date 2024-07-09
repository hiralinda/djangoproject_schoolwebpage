from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create the Profile associated with the user
        profile = Profile.objects.create(user=instance)
        
        # Initialize fields based on user type
        if instance.user_type == 'teacher':
            profile.certifications = ''  # Default empty value or a placeholder
            profile.years_of_experience = 0
            profile.specialization = ''
            profile.education = ''
            profile.teaching_style = ''
        elif instance.user_type == 'student':
            profile.grade = ''
            profile.subjects_of_interest = ''
            profile.learning_goals = ''
        
        profile.save()

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # Save the Profile when the CustomUser is saved
    instance.profile.save()
