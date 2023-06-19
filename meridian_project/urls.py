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
from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('meridian_app.urls')),
]

# old
# from django.contrib.auth import views as auth_views
# from meridian_app.views import HomePageView, RegisterView, TestHomePageView, about, projects, news_and_ideas, careers
# urlpatterns = [
#     path('', TestHomePageView.as_view(), name='index'),
#     # path('', HomePageView.as_view(), name='home'),
#     path('about/', about, name='about'),
#     path('projects/', projects, name='projects'),
#     path('news_and_ideas/', news_and_ideas, name='news_and_ideas'),
#     path('careers/', careers, name='careers'),
#     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('register/', RegisterView.as_view(), name='register'),
#     path('admin/', admin.site.urls),
#     path('meridian_app/', include('meridian_app.urls')),
# ]

