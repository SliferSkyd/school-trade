# my_web/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('my_app.urls')),  # Thay 'my_app' bằng tên app thực tế
    path('bibi/', include('bank.urls'))
]
