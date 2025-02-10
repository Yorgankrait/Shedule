from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Schedule, Event, EventFile
from datetime import datetime
import calendar
from dateutil.relativedelta import relativedelta
from django.http import FileResponse, HttpResponse
from .utils import generate_schedule_pdf
import os
from urllib.parse import quote

# Русские названия месяцев
MONTHS_RU = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
    5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
    9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}

def schedule_list(request):
    """Представление для отображения последнего доступного расписания"""
    schedules = Schedule.objects.all().order_by('-date', 'lesson_number')
    
    # Получаем списки учителей отдельно для заменяемых и заменяющих
    replaced_teachers = set(Schedule.objects.values_list('teacher_replaced', flat=True))
    replacing_teachers = set(Schedule.objects.values_list('teacher_replacing', flat=True))
    all_teachers = sorted(replaced_teachers | replacing_teachers)

    # Получаем выбранных учителей из параметров запроса
    selected_replaced = request.GET.get('replaced_teacher', '')
    selected_replacing = request.GET.get('replacing_teacher', '')
    
    if selected_replaced:
        schedules = schedules.filter(teacher_replaced=selected_replaced)
    if selected_replacing:
        schedules = schedules.filter(teacher_replacing=selected_replacing)
    
    latest_date = schedules.first().date if schedules.exists() else None
    
    if latest_date and not (selected_replaced or selected_replacing):
        schedules = schedules.filter(date=latest_date)
    
    return render(request, 'schedule_app/schedule_list.html', {
        'schedules': schedules,
        'current_date': latest_date,
        'all_teachers': all_teachers,
        'replaced_teachers': sorted(replaced_teachers),
        'replacing_teachers': sorted(replacing_teachers),
        'selected_replaced': selected_replaced,
        'selected_replacing': selected_replacing
    })

def calendar_view(request):
    """Представление для отображения календаря"""
    # Получаем параметры месяца и года из GET-запроса или используем текущую дату
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))
    
    # Создаем объект даты для навигации
    current_date = datetime(year, month, 1)
    prev_month = current_date - relativedelta(months=1)
    next_month = current_date + relativedelta(months=1)
    
    # Проверяем, находится ли дата в допустимом диапазоне (2025-02 - 2026-12)
    min_date = datetime(2025, 2, 1)
    max_date = datetime(2026, 12, 31)
    
    show_prev = current_date > min_date
    show_next = current_date < max_date
    
    # Получаем календарь на текущий месяц
    cal = calendar.monthcalendar(year, month)
    
    # Получаем даты, на которые есть расписание
    scheduled_dates = set(
        schedule.date.strftime('%Y-%m-%d') 
        for schedule in Schedule.objects.all()
    )
    
    return render(request, 'schedule_app/calendar.html', {
        'calendar': cal,
        'scheduled_dates': scheduled_dates,
        'current_year': year,
        'current_month': month,
        'month_name': MONTHS_RU[month],
        'prev_month': prev_month,
        'next_month': next_month,
        'show_prev': show_prev,
        'show_next': show_next,
        'prev_month_name': MONTHS_RU[prev_month.month],
        'next_month_name': MONTHS_RU[next_month.month]
    })

def schedule_by_date(request, date):
    """Представление для отображения расписания на конкретную дату"""
    try:
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        schedules = Schedule.objects.filter(date=selected_date).order_by('lesson_number')
        
        # Получаем список всех учителей
        teachers = set()
        for schedule in Schedule.objects.all():
            teachers.add(schedule.teacher_replaced)
            teachers.add(schedule.teacher_replacing)
        teachers = sorted(teachers)

        # Получаем выбранного учителя из параметров запроса
        selected_teacher = request.GET.get('teacher', '')
        
        if selected_teacher:
            schedules = schedules.filter(
                Q(teacher_replaced=selected_teacher) | 
                Q(teacher_replacing=selected_teacher)
            )
        
        return render(request, 'schedule_app/schedule_by_date.html', {
            'schedules': schedules,
            'selected_date': selected_date,
            'teachers': teachers,
            'selected_teacher': selected_teacher
        })
    except ValueError:
        return render(request, 'schedule_app/error.html', {
            'message': 'Неверный формат даты'
        })

def event_list(request):
    events = Event.objects.all().order_by('-date', '-time')
    return render(request, 'schedule_app/event_list.html', {
        'events': events
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'schedule_app/event_detail.html', {
        'event': event
    })

def home(request):
    """Представление для главной страницы"""
    # Получаем последние замены
    latest_schedules = Schedule.objects.all().order_by('-date', 'lesson_number')[:5]
    
    # Получаем последние важные мероприятия
    latest_events = Event.objects.all().order_by('-date', '-time')[:4]
    
    return render(request, 'schedule_app/home.html', {
        'latest_schedules': latest_schedules,
        'latest_events': latest_events
    })

def download_schedule_pdf(request, date=None):
    """Скачивание расписания в PDF"""
    if date:
        schedules = Schedule.objects.filter(date=date).order_by('lesson_number')
    else:
        latest_date = Schedule.objects.latest('date').date
        schedules = Schedule.objects.filter(date=latest_date).order_by('lesson_number')
    
    filename = generate_schedule_pdf(schedules, date)
    
    # Открываем файл и создаем FileResponse
    response = FileResponse(
        open(filename, 'rb'),
        content_type='application/force-download'
    )
    
    # Кодируем имя файла для корректного отображения русских букв
    encoded_filename = quote(filename)
    response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'
    
    # Добавляем заголовки для принудительного скачивания
    response['X-Sendfile'] = filename
    response['Content-Length'] = os.path.getsize(filename)
    
    # Удаляем временный файл после отправки
    os.remove(filename)
    
    return response 