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
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date, time
from django.http import HttpResponseRedirect


class HomePageView(View):
    def get(self, request):
        return render(request, 'home.html')
    
class LogHoursView(View):
    @method_decorator(login_required)
    def get(self, request):
        try:
            clock_in = ClockIn.objects.filter(employee=request.user).latest('time')
            status = clock_in.status
        except ObjectDoesNotExist:
            status = 'OUT'
        return render(request, 'loghours.html', {'status': status})
    # @method_decorator(login_required)
    # def post(self, request):
    #     if 'clock_in' in request.POST:
    #         return redirect('clock_in')
    #     elif 'meal_break' in request.POST:
    #         return redirect('meal_break')
    #     elif 'clock_out' in request.POST:
    #         return redirect('clock_out')
    #     else:
    #         return HttpResponse('Invalid form submission')
    
class EmployeeLoginView(LoginView):
    template_name = 'employee-login.html'

    def get_success_url(self):
        return '/employee-login/loghours/'  # Specify the URL to redirect to upon successful login

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)

class ClockInView(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            clock_in = ClockIn.objects.filter(employee=request.user).latest('time')
            if clock_in.status == 'IN':
                messages.error(request, 'You are already clocked in, please clock out before logging more hours.')
            else:
                clock_in.status = 'IN'
                clock_in.time = timezone.now()
                clock_in.save()
                messages.success(request, 'You have successfully clocked in.')
        except ObjectDoesNotExist:
            clock_in = ClockIn(employee=request.user, status='IN', time=timezone.now())
            clock_in.save()
            messages.info(request, 'First Clock-In')
        return redirect('loghours')


class MealBreakView(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            clock_in = ClockIn.objects.filter(employee=request.user).latest('time')
            if clock_in.status != 'IN':
                messages.error(request, 'You are not clocked in.')
            else:
                clock_in.status = 'BREAK'
                clock_in.meal_break_time = timezone.now()
                clock_in.save()
                messages.success(request, 'You are now on a meal break.')
        except ObjectDoesNotExist:
            messages.error(request, 'You are not clocked in.')
        return redirect('loghours')

    
class ClockOutView(View):
    @method_decorator(login_required)
    def post(self, request):
        try:
            clock_in = ClockIn.objects.filter(employee=request.user).latest('time')
            if clock_in.status != 'IN':
                messages.error(request, 'You are not clocked in.')
            else:
                if clock_in.status == 'BREAK':
                    messages.error(request, 'You cannot clock out while on a meal break.')
                else:
                    clock_in.status = 'OUT'
                    clock_in.clock_out_time = timezone.now()
                    if clock_in.status == 'BREAK':
                        # Handle the case where there was a meal break
                        meal_break = clock_in.meal_break_time
                        if meal_break is not None:
                            duration_without_break = meal_break - clock_in.time
                            duration_with_break = clock_in.clock_out_time - clock_in.time
                            clock_in.duration = duration_without_break + duration_with_break
                    else:
                        clock_in.duration = clock_in.clock_out_time - clock_in.time
                    clock_in.job_notes = request.POST.get('job_notes', '')
                    clock_in.job_costs = request.POST.get('job_costs', '')
                    clock_in.save()
                    messages.success(request, 'You have successfully clocked out.')

                    # Fetch all ClockIn instances for the current day
                    today_min = datetime.combine(date.today(), time.min)
                    today_max = datetime.combine(date.today(), time.max)
                    todays_clock_ins = ClockIn.objects.filter(employee=request.user, time__range=(today_min, today_max))

                    return render(request, 'loghours.html', {'clock_ins': todays_clock_ins})
        except DatabaseError:
            messages.error(request, 'You are not clocked in.')
            return render(request, 'loghours.html')
        return HttpResponseRedirect('/loghours/')


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
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
        message = request.POST.get('message')

        send_mail(
            'Contact form submission from ' + name,
            'Message:\n' + message,
            email,
            ['ethansmasters@outlook.com'],  # Replace with your email
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

def profile(request):
    return render(request, 'profile.html')

def LoginIn(request):
    return render(request, 'login.html')
