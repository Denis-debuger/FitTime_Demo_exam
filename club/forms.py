import re

from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Booking, Training


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Имя')
    phone = forms.CharField(label='Телефон')
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'phone',
            'email',
        ]
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'email': 'Email',
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        if not re.fullmatch(r'[A-Za-z0-9]{6,}', username):
            raise forms.ValidationError('Логин: минимум 6 символов, латиница и цифры')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Такой логин уже есть')

        return username

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8:
            raise forms.ValidationError('Пароль минимум 8 символов')

        return password

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if not re.fullmatch(r'[А-Яа-яЁё\s-]+', first_name):
            raise forms.ValidationError('Имя должно быть на кириллице')

        return first_name

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if not re.fullmatch(r'8 \(\d{3}\) \d{3}-\d{2}-\d{2}', phone):
            raise forms.ValidationError('Телефон: 8 (XXX) XXX-XX-XX')

        return phone


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'training',
            'visit_at',
            'visit_type',
            'comment',
        ]
        widgets = {
            'visit_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['training'].queryset = Training.objects.filter(is_available=True)

    def clean_visit_at(self):
        dt = self.cleaned_data['visit_at']

        if dt <= timezone.now():
            raise forms.ValidationError('Дата уже прошла')

        return dt
