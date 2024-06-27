from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect


# Create your views here.
# request -> response
# request handler

def index(request):
    return render(request, 'hira/index.html')

def home_view(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data.get('user_type')
            access_code = form.cleaned_data.get('access_code')
            
            # Here you would typically validate the access code
            if validate_access_code(user_type, access_code):
                user.save()
                login(request, user)
                return redirect('home')  
            else:
                form.add_error('access_code', 'Invalid access code for the selected user type.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'hira/signup.html', {'form': form})

def validate_access_code(user_type, access_code):
    # Implement your access code validation logic here
    # For example:
    valid_codes = {
        'student': ['STUDENT2023', 'STUDENT2024'],
        'teacher': ['TEACHER2023', 'TEACHER2024']
    }
    return access_code in valid_codes.get(user_type, [])

def teacher_home(request):
    return render(request, 'hira/teacher_home.html')

def student_home(request):
    return render(request, 'hira/student_home.html')

def home(request):
    if request.user.is_authenticated:
        if request.user.profile.is_teacher:
            return render(request, 'hira/teacher_home.html')
        else:
            return render(request, 'hira/student_home.html')
    return render(request, 'hira/index.html')

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'hira/login.html', {'form': form})

def custom_logout(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('home')  

