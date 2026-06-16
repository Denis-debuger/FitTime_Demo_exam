from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import BookingForm, RegisterForm
from .models import Booking, Profile, Training


def make_admin():
    user, created = User.objects.get_or_create(username='Admin', defaults={'email': 'admin@fittime.local', 'is_staff': True, 'is_superuser': True})
    if created or not user.check_password('FitTimeAdmin'):
        user.set_password('FitTimeAdmin')
    user.is_staff = True
    user.is_superuser = True
    user.save()


def home(request):
    make_admin()
    return render(request, 'club/home.html')


def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
        Profile.objects.create(user=user, name=form.cleaned_data['name'], phone=form.cleaned_data['phone'])
        login(request, user)
        return redirect('trainings')
    return render(request, 'club/register.html', {'form': form})


def login_view(request):
    make_admin()
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('admin_panel' if user.username == 'Admin' else 'trainings')
        messages.error(request, 'Некорректный логин или пароль.')
    return render(request, 'club/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def trainings(request):
    return render(request, 'club/trainings.html', {'trainings': Training.objects.all()})


@login_required
def booking_create(request):
    initial = {}
    if request.GET.get('training'):
        initial['training'] = get_object_or_404(Training, pk=request.GET['training'])
    form = BookingForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.client = request.user
        booking.status = 'new'
        booking.save()
        messages.success(request, 'Запись создана со статусом «Новая».')
        return redirect('cabinet')
    return render(request, 'club/booking_form.html', {'form': form})


@login_required
def cabinet(request):
    return render(request, 'club/cabinet.html', {'bookings': Booking.objects.filter(client=request.user)})


def is_demo_admin(user):
    return user.is_authenticated and user.username == 'Admin'


@login_required
def admin_panel(request):
    if not is_demo_admin(request.user):
        return redirect('home')
    return render(request, 'club/admin_panel.html', {'bookings': Booking.objects.select_related('client', 'client__profile', 'training')})


@require_POST
@login_required
def change_status(request, pk):
    if not is_demo_admin(request.user):
        return redirect('home')
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = request.POST.get('status', booking.status)
    booking.save()
    return redirect('admin_panel')
