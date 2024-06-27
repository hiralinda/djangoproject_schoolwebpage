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