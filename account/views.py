from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def Home(request):
    return render(request, 'index.html')

def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            username = User.objects.get(email=email)

        except User.DoesNotExist:
            error = "Email not found"
            return render(request, "login.html", {"error": error})
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {"error": "Invalid login!"})

    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('home')