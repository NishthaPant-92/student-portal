from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DailyActivity

def home_view(request):
    return render(request, 'home.html')
def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'auth/signup.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    return render(request, 'auth/dashboard.html')
@login_required
def schedule_view(request):
    recommendation = None
    stress_status = None

    if request.method == "POST":
        screen_time = float(request.POST.get("screen_time"))
        study_time = float(request.POST.get("study_time"))

        if screen_time > 1 and study_time > 2:
            stress_status = "High Stress"
            recommendation = """
            • Take 20 min walk
            • Practice 10 min meditation
            • Reduce screen time
            • Add relaxation activity
            """
        else:
            stress_status = "Normal"
            recommendation = "Your routine looks balanced."

    return render(request, "schedule.html", {
        "recommendation": recommendation,
        "stress_status": stress_status
    })



# Create your views here.
