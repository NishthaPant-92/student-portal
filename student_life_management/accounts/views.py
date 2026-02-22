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

    latest = DailyActivity.objects.filter(
        user=request.user
    ).order_by("-id").first()

    screen_time = 0
    study_time = 0
    total_time = 0
    stress_status = None

    if latest:
        screen_time = latest.screen_time
        study_time = latest.study_time
        total_time = screen_time + study_time
        stress_status = latest.stress_status

    return render(request, "auth/dashboard.html", {
        "screen_time": screen_time,
        "study_time": study_time,
        "total_time": total_time,
        "stress_status": stress_status
    })
@login_required
def schedule_view(request):

    if request.method == "POST":

        wake_up = request.POST.get("wake_up")
        sleep = request.POST.get("sleep")
        breakfast = request.POST.get("breakfast")
        lunch = request.POST.get("lunch")
        dinner = request.POST.get("dinner")

        screen_time = float(request.POST.get("screen_time", 0))
        study_time = float(request.POST.get("study_time", 0))

        # Stress logic
        if screen_time >= 4:
            stress_status = "High"
        elif screen_time + study_time >= 6:
            stress_status = "Moderate"
        else:
            stress_status = "Low"

        # Save
        DailyActivity.objects.create(
            user=request.user,
            wake_up_time=wake_up,
            sleep_time=sleep,
            breakfast_time=breakfast,
            lunch_time=lunch,
            dinner_time=dinner,
            screen_time=screen_time,
            study_time=study_time,
            stress_status=stress_status
        )

        return redirect("dashboard")   

    return render(request, "schedule.html")
@login_required
def stress_check_view(request):
    latest = DailyActivity.objects.filter(
        user=request.user
    ).order_by("-id").first()

    return render(request, "stress_check.html", {
        "latest": latest
    })


# Create your views here.
