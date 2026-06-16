import re
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Booking, Training


class RegisterForm(forms.Form):
    username = forms.CharField(label='Логин', min_length=6)
    password = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput)
    name = forms.CharField(label='Имя')
    phone = forms.CharField(label='Телефон')
    email = forms.EmailField(label='Email')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.fullmatch(r'[A-Za-z0-9]{6,}', username):
            raise forms.ValidationError('Логин: минимум 6 символов, только латиница и цифры.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такой логин уже занят.')
        return username

    def clean_name(self):
        name = self.cleaned_data['name']
        if not re.fullmatch(r'[А-Яа-яЁё\s-]+', name):
            raise forms.ValidationError('Имя должно быть на кириллице.')
        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.fullmatch(r'8 \(\d{3}\) \d{3}-\d{2}-\d{2}', phone):
            raise forms.ValidationError('Формат телефона: 8 (XXX) XXX-XX-XX.')
        return phone


class BookingForm(forms.ModelForm):
    visit_at = forms.DateTimeField(label='Дата и время', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), input_formats=['%Y-%m-%dT%H:%M'])

    class Meta:
        model = Booking
        fields = ['training', 'visit_at', 'visit_type', 'comment']
        labels = {'training': 'Тренировка', 'visit_type': 'Тип посещения', 'comment': 'Комментарий'}
        widgets = {'comment': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['training'].queryset = Training.objects.filter(is_available=True)

    def clean_visit_at(self):
        visit_at = self.cleaned_data['visit_at']
        if visit_at <= timezone.now():
            raise forms.ValidationError('Нельзя записаться на прошедшую дату и время.')
        return visit_at
