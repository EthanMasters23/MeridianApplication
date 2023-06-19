from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from .models import ClockIn
from .forms import CustomUserCreationForm
from django.db import DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))


class LogHoursView(View):
    @method_decorator(login_required)
    def get(self, request):
        try:
            clock_in = ClockIn.objects.filter(employee=request.user).latest('time')
            status = clock_in.status
        except ObjectDoesNotExist:
            status = 'OUT'
        return render(request, 'loghours.html', {'status': status})

# class EmployeeLoginView(LoginView):
#     def get(self, request):
#         return render(request, 'login.html')
    
class EmployeeLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'

class ClockInView(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            clock_in = ClockIn.objects.filter(employee=request.user).latest('time')
            if clock_in.status == 'IN':
                messages.error(request, 'You are already clocked in, please clock-out before logging more hours.')
            else:
                clock_in.status = 'IN'
                clock_in.time = timezone.now()
                clock_in.save()
                messages.success(request, 'You have successfully clocked in.')
        except ObjectDoesNotExist:
            clock_in = ClockIn(employee=request.user, status='IN', time=timezone.now())
            clock_in.save()
            messages.info(request, 'First Clock-In')
        return render(request, 'loghours.html')

class MealBreakView(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            clock_in = ClockIn.objects.filter(employee=request.user).latest('time')
            if clock_in.status != 'IN':
                messages.error(request, 'You are not clocked in.')
            else:
                clock_in.status = 'BREAK'
                clock_in.save()
                messages.success(request, 'You are now on break.')
        except ObjectDoesNotExist:
            messages.error(request, 'You are not clocked in.')
        return render(request, 'loghours.html')

class ClockOutView(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            clock_in = ClockIn.objects.filter(employee=request.user).latest('time')
            if clock_in.status != 'IN':
                messages.error(request, 'You are not clocked in.')
            else:
                clock_in.status = 'OUT'
                clock_in.clock_out_time = timezone.now()  # Use timezone-aware datetime
                clock_in.duration = clock_in.clock_out_time - clock_in.time
                clock_in.job_notes = request.POST.get('job_notes', '')
                clock_in.job_costs = request.POST.get('job_costs', '')
                clock_in.save()
                messages.success(request, 'You have successfully clocked out.')

                # Fetch all ClockIn instances for the current day
                today_min = datetime.combine(date.today(), time.min)
                today_max = datetime.combine(date.today(), time.max)
                todays_clock_ins = ClockIn.objects.filter(employee=request.user, time__range=(today_min, today_max))

                return render(request, 'clock_out.html', {'clock_ins': todays_clock_ins})
        except DatabaseError:
            messages.error(request, 'You are not clocked in.')
            return render(request, 'loghours.html')


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})
    

class UserInfoView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CustomUserCreationForm(instance=request.user)
        return render(request, 'user_info.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = CustomUserCreationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'user_info.html', {'form': form})


@csrf_exempt
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        send_mail(
            'Contact form submission from ' + name,
            'Phone number: ' + phone_number + '\nMessage:\n' + message,
            email,
            ['your-email@example.com'],  # Replace with your email
            fail_silently=True,
        )

        return HttpResponse('Email sent')
    else:
        return HttpResponse('Method not allowed', status=405)


def about(request):
    return render(request, 'about.html')

def projects(request):
    return render(request, 'projects.html')

def news_and_ideas(request):
    return render(request, 'news_and_ideas.html')

def careers(request):
    return render(request, 'careers.html')
