from django.contrib import admin
from .models import Schedule, Event, EventFile

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date', 'class_number', 'lesson_number', 'subject', 
                   'teacher_replaced', 'teacher_replacing')
    list_filter = ('date', 'class_number', 'subject')
    search_fields = ('class_number', 'subject', 'teacher_replaced', 
                    'teacher_replacing', 'comment')
    ordering = ('-date', 'lesson_number')

class EventFileInline(admin.TabularInline):
    model = EventFile
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'is_important', 'created_at')
    list_filter = ('date', 'is_important')
    search_fields = ('title', 'description')
    inlines = [EventFileInline] 