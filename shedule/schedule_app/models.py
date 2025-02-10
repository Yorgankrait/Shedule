from django.db import models
from django.utils import timezone

class Schedule(models.Model):
    date = models.DateField('Дата')
    class_number = models.CharField('Класс', max_length=10)
    classroom = models.CharField('Кабинет', max_length=10)
    lesson_time = models.TimeField('Время урока')
    lesson_number = models.IntegerField('Номер урока')
    subject = models.CharField('Предмет', max_length=100)
    teacher_replaced = models.CharField('Кого заменяют', max_length=100)
    teacher_replacing = models.CharField('Кто заменяет', max_length=100)
    comment = models.TextField('Комментарий', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        ordering = ['-date', 'lesson_number']

    def __str__(self):
        return f"{self.date} - {self.class_number} - {self.lesson_number} урок"

class Event(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание')
    date = models.DateField('Дата мероприятия')
    time = models.TimeField('Время мероприятия', null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_important = models.BooleanField('Важное', default=False)
    
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['-date', '-time']

    def __str__(self):
        return self.title

class EventFile(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='files')
    file = models.FileField('Файл', upload_to='event_files/%Y/%m/%d/')
    file_name = models.CharField('Название файла', max_length=255)
    uploaded_at = models.DateTimeField('Дата загрузки', auto_now_add=True)

    class Meta:
        verbose_name = 'Файл мероприятия'
        verbose_name_plural = 'Файлы мероприятий'

    def __str__(self):
        return self.file_name

    @property
    def file_extension(self):
        return self.file.name.split('.')[-1].lower()

    @property
    def is_image(self):
        return self.file_extension in ['jpg', 'jpeg', 'png', 'gif']

    @property
    def is_document(self):
        return self.file_extension in ['pdf', 'doc', 'docx', 'xls', 'xlsx'] 