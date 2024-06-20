from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.

def Home(request):
    return render(request, 'index.html')

def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            error = 'Username already taken, try another!'
            return render(request, 'register.html', {"error": error})
        if User.objects.filter(email=email).exists():
            error = 'Email already registered, try login!'
            return render(request, 'register.html', {"error": error})
            
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        user_profile = Profile.objects.create(user=new_user)

        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile = Profile.objects.get(user=user)
            if profile.active:
                return redirect('home')
            else:
                return redirect('verify')
        else:
            return render(request, 'register.html', {"error": "Something went wrong! Try again later."})

    return render(request, 'register.html')


def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            error = "Email not found"
            return render(request, "login.html", {"error": error})
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            profile = Profile.objects.get(user=user)
            if profile.active:
                return redirect('home')
            else:
                return redirect('verify')
        else:
            return render(request, 'login.html', {"error": "Invalid login!"})

    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('home')

def verifyMessage(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if profile.active:
        return redirect('home')
    else:
        domain = get_current_site(request).domain
        verification_link = f'http://{domain}/verify/{profile.auth_token}/'

        # Email content
        subject = 'Verify your email address'
        html_message = render_to_string('verification_email.html', {'verification_link': verification_link})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER  # Update with your email address
        to_email = profile.user.email

        # Send email
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

    return render(request, 'verify.html')

def verify_account(request, auth_token):
    profile = get_object_or_404(Profile, auth_token=auth_token)
    
    if not profile.active:
        profile.active = True
        profile.save()
        return render(request, 'account_verified.html')
    else:
        return render(request, "account_already_verified.html")