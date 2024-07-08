from .models import Profile, TeacherProfile, StudentProfile, CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from hira.models import CustomUser, Message

class CustomUserCreationForm(UserCreationForm):
    USER_TYPES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPES, widget=forms.RadioSelect)
    # access_code = forms.CharField(max_length=50, required=True, help_text='Enter your student or teacher access code')

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'user_type',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['access_code'].widget.attrs.update({'class': 'form-input'})


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            })
        self.fields['bio'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })
        
class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['certifications', 'years_of_experience', 'specialization', 'education', 'teaching_style']

class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['grade', 'subjects_of_interest', 'learning_goals']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'message']