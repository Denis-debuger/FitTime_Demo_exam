from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def seed_trainings(apps, schema_editor):
    Training = apps.get_model('club', 'Training')
    Training.objects.bulk_create([
        Training(title='Силовая тренировка', description='Упражнения для силы и тонуса мышц.', price=900, duration=60, is_available=True),
        Training(title='Йога', description='Растяжка, дыхание и спокойная нагрузка.', price=700, duration=50, is_available=True),
        Training(title='Кардио', description='Интенсивная тренировка для выносливости.', price=800, duration=45, is_available=True),
    ])

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Training', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('title', models.CharField(max_length=120, verbose_name='Название')), ('description', models.TextField(verbose_name='Описание')), ('price', models.PositiveIntegerField(verbose_name='Стоимость')), ('duration', models.PositiveIntegerField(verbose_name='Длительность, мин')), ('is_available', models.BooleanField(default=True, verbose_name='Доступна'))]),
        migrations.CreateModel(name='Profile', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('name', models.CharField(max_length=80, verbose_name='Имя')), ('phone', models.CharField(max_length=18, verbose_name='Телефон')), ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='Review', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('text', models.TextField(verbose_name='Отзыв')), ('created_at', models.DateTimeField(auto_now_add=True)), ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)), ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.training'))]),
        migrations.CreateModel(name='Booking', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')), ('visit_at', models.DateTimeField(verbose_name='Дата и время')), ('visit_type', models.CharField(choices=[('first', 'Первичное'), ('repeat', 'Повторное')], max_length=10, verbose_name='Тип посещения')), ('comment', models.TextField(blank=True, verbose_name='Комментарий')), ('status', models.CharField(choices=[('new', 'Новая'), ('confirmed', 'Подтверждена'), ('visited', 'Клиент посетил тренировку'), ('done', 'Тренировка проведена'), ('cancelled', 'Отменена')], default='new', max_length=20, verbose_name='Статус')), ('created_at', models.DateTimeField(auto_now_add=True)), ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)), ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.training'))], options={'ordering': ['-visit_at']}),
        migrations.RunPython(seed_trainings),
    ]
