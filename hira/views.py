from django.shortcuts import render

# Create your views here.
# request -> response
# request handler

def index(request):
    return render(request, 'index.html')

def home_view(request):
    return render(request, 'home.html')