from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from hira.models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    USER_TYPES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPES, widget=forms.RadioSelect)
    access_code = forms.CharField(max_length=50, required=True, help_text='Enter your student or teacher access code')

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'user_type', 'access_code')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['access_code'].widget.attrs.update({'class': 'form-input'})

        from django import forms
from .models import Profile, TeacherProfile, StudentProfile, CustomUser

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    languages = forms.MultipleChoiceField(
        choices=Profile.LANGUAGE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Profile
        fields = ['bio', 'languages']

class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['certifications', 'years_of_experience', 'specialization', 'education', 'teaching_style']

class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['grade', 'subjects_of_interest', 'learning_goals']