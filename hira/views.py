from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import Profile, CustomUser, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

# Create your views here.
# request -> response
# request handler

def index(request):
    teachers = CustomUser.objects.filter(user_type='teacher')
    context = {'teachers': teachers}
    return render(request, 'hira/index.html', context)


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'hira/teacher_home.html')
        elif request.user.is_student:
            return render(request, 'hira/student_home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home page or another page after successful sign-up
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home') 

def custom_logout(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        
        return redirect('home')  

@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'hira/edit_profile.html', {'form': form})

def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    return render(request, 'hira/profile.html', {'profile': profile})

@login_required
def browse_teachers(request):
    teachers = Profile.objects.filter(user__user_type='teacher')
    return render(request, 'hira/browse_teachers.html', {'teachers': teachers})

@login_required
def inbox(request, user_id=None):
    conversations = []
    messages = Message.objects.filter(sender=request.user) | Message.objects.filter(receiver=request.user)
    conversations_dict = {}
    
    for message in messages:
        if message.sender == request.user:
            participant = message.receiver
        else:
            participant = message.sender

        if participant not in conversations_dict:
            conversations_dict[participant] = {'participant': participant, 'last_message': message.message}
        else:
            conversations_dict[participant]['last_message'] = message.message

    conversations = list(conversations_dict.values())

    active_conversation = None
    if user_id:
        active_user = get_object_or_404(CustomUser, id=user_id)
        active_conversation = {
            'participant': active_user,
            'messages': messages.filter(sender=active_user) | messages.filter(receiver=active_user).order_by('timestamp')
        }

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text and active_conversation:
            Message.objects.create(sender=request.user, receiver=active_conversation['participant'], message=message_text)
            return redirect('inbox', user_id=active_conversation['participant'].id)

    return render(request, 'hira/inbox.html', {'conversations': conversations, 'active_conversation': active_conversation})
@login_required
def send_message(request, user_id):
    recipient = get_object_or_404(CustomUser, id=user_id)
    
    if request.user.is_teacher:
        return redirect('profile', user_id=user_id)
    
    if request.method == 'POST':
        message_text = "Hi, I would like to contact you."  # Initial message when student clicks "Contact"
        Message.objects.create(sender=request.user, receiver=recipient, message=message_text)
        
        return redirect('inbox', user_id=recipient.id)

    return redirect('profile', user_id=user_id)