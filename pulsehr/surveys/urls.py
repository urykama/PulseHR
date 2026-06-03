from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_list, name='survey_list'),
    path('<int:survey_id>/', views.survey_detail, name='survey_detail'),
    path('thanks/', views.survey_thanks, name='survey_thanks'),
    path('results/<int:survey_id>/', views.survey_results, name='survey_results'),
    path('hr/surveys/', views.survey_list_hr, name='survey_list_hr'),
    path('logout/', views.custom_logout, name='custom_logout'),  # <-- добавляем
    path('logout/success/', views.logout_success, name='custom_logout_success'),  # <-- добавляем
]
