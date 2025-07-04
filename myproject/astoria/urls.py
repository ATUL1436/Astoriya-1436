from django.contrib import admin
from django.urls import path,include
from . import views
from django.shortcuts import render

urlpatterns = [
    path('', lambda request: render(request, 'index.html'), name='home'),
    path('submit/', views.submit_lead, name='submit_lead'),
]