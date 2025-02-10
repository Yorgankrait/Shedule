from django.urls import path
from . import views

app_name = 'schedule_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('schedule/', views.schedule_list, name='schedule_list'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('schedule/<str:date>/', views.schedule_by_date, name='schedule_by_date'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('download-pdf/', views.download_schedule_pdf, name='download_pdf'),
    path('download-pdf/<str:date>/', views.download_schedule_pdf, name='download_pdf_by_date'),
] 