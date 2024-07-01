from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile, TeacherProfile, StudentProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        if instance.user_type == 'teacher':
            TeacherProfile.objects.create(profile=profile)
        elif instance.user_type == 'student':
            StudentProfile.objects.create(profile=profile)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    if hasattr(instance.profile, 'teacherprofile'):
        instance.profile.teacherprofile.save()
    elif hasattr(instance.profile, 'studentprofile'):
        instance.profile.studentprofile.save()
