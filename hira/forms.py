from .models import Profile, CustomUser
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

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'user_type',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ProfileUpdateForm(forms.ModelForm):
    languages = forms.MultipleChoiceField(
        choices=Profile.LANGUAGE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Profile
        fields = [
            'bio', 'languages', 
            'certifications', 'years_of_experience', 'specialization', 'education', 'teaching_style', 
            'grade', 'subjects_of_interest', 'learning_goals'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            })
        self.fields['bio'].widget.attrs.update({
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
        })

    def clean(self):
        cleaned_data = super().clean()
        user_type = self.instance.user.user_type

        if user_type == 'teacher':
            self.fields['certifications'].required = False
            self.fields['years_of_experience'].required = False
            self.fields['specialization'].required = False
            self.fields['education'].required = False
            self.fields['teaching_style'].required = False
       
        elif user_type == 'student':
            
            self.fields['grade'].required = False
            self.fields['subjects_of_interest'].required = False
            self.fields['learning_goals'].required = False
        else:
            raise forms.ValidationError("Invalid user type.")

        return cleaned_data

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'message']