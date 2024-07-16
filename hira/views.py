# Standard Library Imports
from datetime import datetime, timedelta
import os

# Third-Party Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# Local Imports
from .models import Profile, CustomUser, Message, Availability, ClassSchedule
from .forms import CustomUserCreationForm, ProfileUpdateForm, AvailabilityForm
from django.conf import settings

def index(request):
    teachers = CustomUser.objects.filter(user_type='teacher')
    context = {'teachers': teachers}
    return render(request, 'hira/index.html', context)

def home(request):
    if request.user.is_authenticated:
        return render(request, 'hira/home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
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
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
            
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'hira/edit_profile.html', {'form': form})

def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    availabilities = profile.availabilities.all().order_by('day')
    return render(request, 'hira/profile.html', {
        'profile': profile,
        'availabilities': availabilities,
    })

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
            conversations_dict[participant] = {
                'participant': participant,
                'last_message': message.message,
                'last_message_time': message.timestamp,
                'profile_name': participant.profile.name,
                'profile_picture': participant.profile.profile_picture.url if participant.profile.profile_picture else None,
                'unread': not message.read and message.receiver == request.user
            }
        else:
            conversations_dict[participant]['last_message'] = message.message
            conversations_dict[participant]['last_message_time'] = message.timestamp
            conversations_dict[participant]['unread'] = conversations_dict[participant]['unread'] or (not message.read and message.receiver == request.user)

    conversations = sorted(conversations_dict.values(), key=lambda x: x['last_message_time'], reverse=True)

    active_conversation = None
    default_message = None
    if user_id:
        active_user = get_object_or_404(CustomUser, id=user_id)
        active_conversation = {
            'participant': active_user,
            'messages': messages.filter(sender=active_user) | messages.filter(receiver=active_user).order_by('timestamp'),
            'profile_name': active_user.profile.name,
            'profile_picture': active_user.profile.profile_picture.url if active_user.profile.profile_picture else None
        }

        active_conversation['messages'].filter(receiver=request.user, read=False).update(read=True)
        unread_messages = active_conversation['messages'].filter(receiver=request.user, read=False)
        unread_messages.update(read=True)

        if request.method == 'POST':
            default_message = "Hi, I would like to contact you."

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text and active_conversation:
            Message.objects.create(sender=request.user, receiver=active_conversation['participant'], message=message_text, read=False)
            return redirect('inbox', user_id=active_conversation['participant'].id)

    return render(request, 'hira/inbox.html', {
        'conversations': conversations,
        'active_conversation': active_conversation,
        'default_message': default_message
    })

@login_required
def availability_view(request):
    profile = request.user.profile
    availabilities = {day: None for day, _ in Availability.DAY_CHOICES}
    for availability in profile.availabilities.all():
        availabilities[availability.day] = availability

    if request.method == 'POST':
        day = request.POST.get('day')
        availability = availabilities[day] or Availability(profile=profile, day=day)
        form = AvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            return redirect('availability')
    else:
        form = AvailabilityForm()

    return render(request, 'hira/availability.html', {
        'profile': profile,
        'availabilities': availabilities,
        'form': form,
        'day_choices': Availability.DAY_CHOICES,
    })


# API HANDLING

SCOPES = ['https://www.googleapis.com/auth/calendar']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def authorize(request):
    flow = Flow.from_client_config({
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }, scopes=SCOPES)

    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    
    print(authorization_url)
    request.session['state'] = state
    # print(state)
    return redirect(authorization_url)

@login_required
def oauth2callback(request):
    state = request.GET.get('state')
    code = request.GET.get('code')
    scope = request.GET.get('scope')
    flow = Flow.from_client_config({
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }, scopes=SCOPES, state=state)
    
    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

    authorization_response = request.build_absolute_uri()
    print("authorization_response", authorization_response)
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    service = build('calendar', 'v3', credentials=credentials)
    profile = service.calendarList().get(calendarId='primary').execute()
    request.user.google_email = profile['id']

    if CustomUser.objects.filter(google_email=request.user.google_email).exists():
        flow = Flow.from_client_config({
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }, scopes=SCOPES)
        
        flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
        authorization_url, _  = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='select_account'
    )
    
        return redirect(authorization_url)
        
    if not request.user.google_credentials:
        request.user.google_credentials = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
        }
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    request.user.save()
    return redirect('schedule_class')


from django.utils import timezone
import pytz

def schedule_class(request):
    if 'credentials' not in request.session and not request.user.google_credentials:
        return redirect('authorize')
    
    if request.user.google_credentials:
        credentials = Credentials(**request.user.google_credentials)
        service = build('calendar', 'v3', credentials=credentials)
       
        if request.method == 'POST':
            # Process the form data
            start_date = request.POST['start_date']
            start_time = request.POST['start_time']
            selected_timezone = request.POST['timezone']
            
            # Create a timezone-aware datetime object
            local_tz = pytz.timezone(selected_timezone)
            start_datetime = (datetime.strptime(f"{start_date} {start_time}", '%Y-%m-%d %H:%M'))
            
            # # Convert to UTC for storage
            # start_datetime_utc = start_datetime.astimezone(pytz.UTC)
            # end_datetime_utc = start_datetime_utc + timedelta(minutes=50)
            
            attendees_ids = request.POST.getlist('attendees')
            attendees = CustomUser.objects.filter(id__in=attendees_ids)
            
            event_db = ClassSchedule.objects.create(
                summary=request.POST['summary'],
                location=request.POST['location'],
                description=request.POST['description'],
                start_datetime=start_datetime,
                end_datetime=start_datetime + timedelta(minutes=50),
                teacher=request.user,
                timezone=selected_timezone
            )
            event_db.attendees.set(attendees)
            event_db.save()

            event = {
                'summary': request.POST['summary'],
                'location': request.POST['location'],
                'description': request.POST['description'],
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': selected_timezone,
                },
                'end': {
                    'dateTime': (start_datetime + timedelta(minutes=50)).isoformat(),
                    'timeZone': selected_timezone,
                },
                'attendees': [
                    {'email': attendee.email} for attendee in attendees
                ],
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            
            return redirect('scheduled_classes')
        
    # If it's a GET request, render the form with default values
    received_messages = Message.objects.filter(receiver=request.user)
    students = CustomUser.objects.filter(id__in=received_messages.values_list('sender', flat=True), user_type='student')

    default_start_date = timezone.now().strftime('%Y-%m-%d')
    default_start_time = timezone.now().strftime('%H:%M')
    default_timezone = request.user.timezone if hasattr(request.user, 'timezone') else 'UTC'

    timezones = pytz.common_timezones
    default_event = {
        'summary': 'HiraLearn Class',
        'location': 'Online',
        'description': 'A class scheduled with HiraLearn',
    }
    return render(request, 'hira/schedule_class.html', {
        'event': default_event,
        'default_start_date': default_start_date,
        'default_start_time': default_start_time,
        'default_timezone': default_timezone,
        'students': students,
        'timezones': timezones
    })

from django.utils import timezone

def scheduled_classes(request):
    if not request.user.is_authenticated:
        return redirect('login')

    now = timezone.now()
    user_id = request.user.id

    # Fetch all classes for the current student
    student_classes = ClassSchedule.objects.filter(
        attendees__in=[request.user]
    ).order_by('start_datetime')

    # Fetch all classes for the current teacher
    teacher_classes = ClassSchedule.objects.filter(
        teacher=request.user
    ).order_by('start_datetime')


    return render(request, 'hira/scheduled_classes.html', {
        'student_classes': student_classes,
        'teacher_classes': teacher_classes,
    })