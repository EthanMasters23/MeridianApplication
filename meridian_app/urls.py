"""
URL configuration for meridian_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomePageView,
    EmployeeLoginView,
    LogHoursView,
    about,
    projects,
    news_and_ideas,
    careers,
    RegisterView,
    UserInfoView,
    ClockInView,
    MealBreakView,
    ClockOutView,
    contact,
)

# app_name = 'meridian_app'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact/', contact, name='contact'),
    path('login/', EmployeeLoginView.as_view(), name='login'),
    path('login/loghours/', LogHoursView.as_view(), name='loghours'),
    path('about/', about, name='about'),
    path('projects/', projects, name='projects'),
    path('news_and_ideas/', news_and_ideas, name='news_and_ideas'),
    path('careers/', careers, name='careers'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user_info/', UserInfoView.as_view(), name='user_info'),
    path('clock_in/', ClockInView.as_view(), name='clock_in'),
    path('meal_break/', MealBreakView.as_view(), name='meal_break'),
    path('clock_out/', ClockOutView.as_view(), name='clock_out'),
]



# old
# from django.urls import path
# from .views import ClockInView, MealBreakView, ClockOutView, UserInfoView, send_email

# urlpatterns = [
#     path('user_info/', UserInfoView.as_view(), name='user_info'),
#     path('clock_in/', ClockInView.as_view(), name='clock_in'),
#     path('meal_break/', MealBreakView.as_view(), name='meal_break'),
#     path('clock_out/', ClockOutView.as_view(), name='clock_out'),
#     path('send_email/', send_email, name='send_email'),
# ]