from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DailyActivity,Expense,Budget
from django.db.models import Sum
from datetime import datetime
from .models import Expense

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
def dashboard_view_main(request):

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

@login_required
def add_expense(request):
    if request.method == "POST":
        Expense.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            amount=float(request.POST.get("amount")),
            category=request.POST.get("category"),
            is_split=request.POST.get("is_split") == "on",
            total_people=request.POST.get("total_people") or None,
        )
        return redirect("expense_dashboard")

    return render(request, "expense/add_expense.html")
from .models import Expense
from django.db.models import Sum


from django.db.models import Sum
from django.db.models.functions import TruncMonth

@login_required
def expense_dashboard(request):

    expenses = Expense.objects.filter(user=request.user)

    total_spent = expenses.aggregate(Sum("amount"))["amount__sum"] or 0

    # 🔹 Get Latest Budget
    latest_budget = Budget.objects.filter(user=request.user).order_by("-created_at").first()
    total_budget = latest_budget.amount if latest_budget else 0

    remaining_budget = total_budget - total_spent

    # 🔹 Category Data (Pie Chart)
    category_data = (
        expenses.values("category")
        .annotate(total=Sum("amount"))
    )

    categories = [item["category"] for item in category_data]
    category_totals = [item["total"] for item in category_data]

    # 🔹 Monthly Data (Bar Chart)
    monthly_data = (
        expenses.annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    months = [item["month"].strftime("%b %Y") for item in monthly_data]
    month_totals = [item["total"] for item in monthly_data]

    context = {
        "expenses": expenses.order_by("-created_at"),
        "total_spent": total_spent,
        "total_budget": total_budget,
        "remaining_budget": remaining_budget,
        "categories": categories,
        "category_totals": category_totals,
        "months": months,
        "month_totals": month_totals,
    }

    return render(request, "expense/expense_dashboard.html", context)
@login_required
def delete_expense(request, id):
    expense = Expense.objects.get(id=id, user=request.user)
    expense.delete()
    return redirect("expense_dashboard")
@login_required
def set_budget(request):

    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        period = request.POST.get("period")

        Budget.objects.create(
            user=request.user,
            amount=amount,
            period=period
        )

        return redirect("expense_dashboard")

    return render(request, "expense/set_budget.html")
@login_required
def dashboard_view(request):
    return render(request, "auth/dashboard.html")

# Create your views here.
