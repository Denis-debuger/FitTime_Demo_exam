from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Имя', max_length=80)
    phone = models.CharField('Телефон', max_length=18)

    def __str__(self):
        return self.name


class Training(models.Model):
    title = models.CharField('Название', max_length=120)
    description = models.TextField('Описание')
    price = models.PositiveIntegerField('Стоимость')
    duration = models.PositiveIntegerField('Длительность, мин')
    is_available = models.BooleanField('Доступна', default=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    VISIT_TYPES = [('first', 'Первичное'), ('repeat', 'Повторное')]
    STATUSES = [
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('visited', 'Клиент посетил тренировку'),
        ('done', 'Тренировка проведена'),
        ('cancelled', 'Отменена'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    visit_at = models.DateTimeField('Дата и время')
    visit_type = models.CharField('Тип посещения', max_length=10, choices=VISIT_TYPES)
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUSES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visit_at']

    def __str__(self):
        return f'{self.client.username} — {self.training.title}'


class Review(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    text = models.TextField('Отзыв')
    created_at = models.DateTimeField(auto_now_add=True)
