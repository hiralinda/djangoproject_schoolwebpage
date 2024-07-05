from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from .models import Profile, CustomUser, TeacherProfile, StudentProfile

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm, TeacherProfileUpdateForm, StudentProfileUpdateForm


# Create your views here.
# request -> response
# request handler

def index(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teacher_home')
        elif request.user.is_student:
            return redirect('student_home')

    teachers = CustomUser.objects.filter(user_type='teacher', is_active=True).select_related('profile__teacherprofile')[:4]
    total_teachers = CustomUser.objects.filter(user_type='teacher', is_active=True).count()
    
    context = {
        'teachers': teachers,
        'total_teachers': total_teachers,
    }
    return render(request, 'hira/index.html', context)


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teacher_home')
        elif request.user.is_student:
            return redirect('student_home')

    teachers = Profile.objects.filter(user__user_type='teacher')
    print(teachers)
    return render(request, 'hira/index.html', {'teachers': teachers})

def teacher_home(request):
    return render(request, 'hira/teacher_home.html')

def student_home(request):
    return render(request, 'hira/student_home.html')

# def home(request):
#     if request.user.is_authenticated:
#         if request.user.profile.is_teacher:
#             return render(request, 'hira/teacher_home.html')
#         else:
#             return render(request, 'hira/student_home.html')
#     return render(request, 'hira/index.html')

# def home_view(request):
#     return render(request, 'home.html')


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
                # Debugging output
                print("Authentication failed: Invalid username and/or password.")
                return render(request, 'hira/login.html', {'form': form, 'message': "Invalid username and/or password."})
    else:
        form = AuthenticationForm()
    # Debugging output
    print("Rendering login form.")
    return render(request, 'hira/login.html', {'form': form})


def custom_logout(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        return redirect('home')  


@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if request.user.user_type == 'teacher':
            teacher_profile, created = TeacherProfile.objects.get_or_create(profile=profile)
            specific_form = TeacherProfileUpdateForm(request.POST, instance=teacher_profile)
        elif request.user.user_type == 'student':
            student_profile, created = StudentProfile.objects.get_or_create(profile=profile)
            specific_form = StudentProfileUpdateForm(request.POST, instance=student_profile)
        else:
            specific_form = None
        
        if user_form.is_valid() and profile_form.is_valid() and (specific_form is None or specific_form.is_valid()):
            user_form.save()
            profile_form.save()
            if specific_form:
                specific_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
        
        if request.user.user_type == 'teacher':
            teacher_profile, created = TeacherProfile.objects.get_or_create(profile=profile)
            specific_form = TeacherProfileUpdateForm(instance=teacher_profile)
        elif request.user.user_type == 'student':
            student_profile, created = StudentProfile.objects.get_or_create(profile=profile)
            specific_form = StudentProfileUpdateForm(instance=student_profile)
        else:
            specific_form = None
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'specific_form': specific_form
    }
    return render(request, 'hira/edit_profile.html', context)

# @login_required
# def profile(request):
#     try:
#         profile = request.user.profile
#     except Profile.DoesNotExist:
#         profile = Profile.objects.create(user=request.user)

#     if request.user.user_type == 'teacher':
#         specific_profile, created = TeacherProfile.objects.get_or_create(profile=profile)
#     elif request.user.user_type == 'student':
#         specific_profile, created = StudentProfile.objects.get_or_create(profile=profile)
#     else:
#         specific_profile = None

#     context = {
#         'user': request.user,
#         'profile': profile,
#         'specific_profile': specific_profile
#     }
#     return render(request, 'hira/profile.html', context)

def profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user_profile = get_object_or_404(Profile, user=user)
    return render(request, 'hira/profile.html', {'user': user, 'profile': user_profile})

@login_required
def browse_teachers(request):
    teachers = Profile.objects.filter(user__user_type='teacher')
    return render(request, 'hira/browse_teachers.html', {'teachers': teachers})

@login_required
def inbox(request):
    # Placeholder for chat functionality
    return render(request, 'hira/inbox.html')