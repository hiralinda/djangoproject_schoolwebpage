from .models import Profile, CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from hira.models import CustomUser, Message, Availability

from django.core.validators import EmailValidator
class CustomUserCreationForm(UserCreationForm):
    USER_TYPES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPES, widget=forms.RadioSelect)
    email = forms.EmailField(
        label='Email',
        max_length=254,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', 'user_type',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput)
    # languages = forms.MultipleChoiceField(
    #     choices=Profile.LANGUAGE_CHOICES,
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )

    class Meta:
        model = Profile
        fields = [
            'name', 'profile_picture', 'bio', 
            'certifications', 'years_of_experience', 'specialization', 'education', 'teaching_style', 
            'grade', 'subjects_of_interest', 'learning_goals'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_type = self.instance.user.user_type

        for field in self.fields.values():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
                })

        if user_type == 'teacher':
            # Remove student-specific fields
            for field in ['grade', 'subjects_of_interest', 'learning_goals']:
                if field in self.fields:
                    del self.fields[field]
        elif user_type == 'student':
            # Remove teacher-specific fields
            for field in ['certifications', 'years_of_experience', 'specialization', 'education', 'teaching_style']:
                if field in self.fields:
                    del self.fields[field]
        else:
            raise forms.ValidationError("Invalid user type.")

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'message']


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['day', 'start_time', 'end_time']
        widgets = {
            'day': forms.Select(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'time'
            }),
        }