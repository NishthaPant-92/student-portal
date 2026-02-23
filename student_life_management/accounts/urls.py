from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view_main, name='dashboard'),
    path('schedule/', views.schedule_view, name='schedule'),
    path("stress-check/", views.stress_check_view, name="stress_check"),
     path("expense/", views.expense_dashboard, name="expense_dashboard"),
    path("expense/add/", views.add_expense, name="add_expense"),
    path("expense/delete/<int:id>/", views.delete_expense, name="delete_expense"),
    path("expense/set-budget/", views.set_budget, name="set_budget"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    


   
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='auth/password_reset.html',
             email_template_name='auth/password_reset_email.html',
         ), 
         name='password_reset'),

    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='auth/password_reset_done.html'
         ), 
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='auth/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),

    path('reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='auth/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]
