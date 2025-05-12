# my_web/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('my_app.urls'))
]
