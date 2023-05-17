"""WorkoutAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from ExercisesApp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exercises/', views.exercise_list, name='exercises'),
    path('exercises/<int:id>/', views.exercise_detail, name='exercise_detail'),
    path('days/', views.day_list, name='days'),
    path('days/<int:id>', views.day_detail, name='day_detail'),
    path('routines/', views.routine_list, name='routines'),
    path('routines/<int:id>', views.routine_detail, name='routine_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
