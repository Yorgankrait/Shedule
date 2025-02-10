from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import os
from django.conf import settings
from datetime import datetime

# Изменим путь к шрифту на системный
font_path = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'  # Для MacOS
pdfmetrics.registerFont(TTFont('Arial', font_path))

def generate_schedule_pdf(schedules, date=None):
    # Преобразуем строку в объект даты, если это строка
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d').date()

    # Создаем буфер для PDF
    filename = f'Замены на {date.strftime("%d.%m.%Y")}.pdf' if date else 'Замены.pdf'
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm
    )

    # Создаем стили
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomTitle',
        fontName='Arial',
        fontSize=16,
        spaceAfter=30,
        alignment=1
    ))
    styles.add(ParagraphStyle(
        name='CustomBody',
        fontName='Arial',
        fontSize=10
    ))

    # Подготавливаем данные
    elements = []
    
    # Добавляем заголовок
    title = 'Замены на ' + date.strftime('%d.%m.%Y') if date else 'Замены'
    elements.append(Paragraph(title, styles['CustomTitle']))
    
    # Создаем таблицу
    table_data = [['Урок', 'Время', 'Класс', 'Кабинет', 'Предмет', 'Кого заменяют', 'Кто заменяет']]
    
    for schedule in schedules:
        table_data.append([
            str(schedule.lesson_number),
            schedule.lesson_time.strftime('%H:%M'),
            schedule.class_number,
            schedule.classroom,
            schedule.subject,
            schedule.teacher_replaced,
            schedule.teacher_replacing
        ])

    # Создаем таблицу
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    
    # Генерируем PDF
    doc.build(elements)
    return filename 