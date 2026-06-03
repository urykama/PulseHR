from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # <-- добавляем эту строчку
    path('', lambda request: redirect('survey_list', permanent=False)),
    path('surveys/', include('surveys.urls')),
]