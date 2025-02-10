from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('class_number', models.CharField(max_length=10, verbose_name='Класс')),
                ('classroom', models.CharField(max_length=10, verbose_name='Кабинет')),
                ('lesson_time', models.TimeField(verbose_name='Время урока')),
                ('lesson_number', models.IntegerField(verbose_name='Номер урока')),
                ('subject', models.CharField(max_length=100, verbose_name='Предмет')),
                ('teacher_replaced', models.CharField(max_length=100, verbose_name='Кого заменяют')),
                ('teacher_replacing', models.CharField(max_length=100, verbose_name='Кто заменяет')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Расписание',
                'verbose_name_plural': 'Расписания',
                'ordering': ['-date', 'lesson_number'],
            },
        ),
    ] 