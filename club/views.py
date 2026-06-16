from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm, RegisterForm
from .models import Booking, Profile, Training


def create_admin():
    admin = User.objects.filter(username='Admin').first()

    if not admin:
        admin = User(username='Admin', email='admin@fittime.local')

    admin.is_staff = True
    admin.is_superuser = True
    admin.set_password('FitTimeAdmin')
    admin.save()


def home(request):
    create_admin()

    return render(request, 'club/home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            Profile.objects.create(
                user=user,
                name=form.cleaned_data['first_name'],
                phone=form.cleaned_data['phone'],
            )

            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'club/register.html', {'form': form})


def login_view(request):
    create_admin()

    form = AuthenticationForm(
        request,
        data=request.POST or None,
    )

    if form.is_valid():
        user = form.get_user()

        login(request, user)

        if user.username == 'Admin':
            return redirect('admin_panel')

        return redirect('trainings')

    return render(request, 'club/login.html', {'form': form})


def logout_view(request):
    logout(request)

    return redirect('home')


@login_required
def trainings(request):
    trainings_list = Training.objects.all()

    return render(request, 'club/trainings.html', {'trainings': trainings_list})


@login_required
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.status = 'new'
            booking.save()
            messages.success(request, 'Запись создана')

            return redirect('cabinet')
    else:
        form = BookingForm(initial={'training': request.GET.get('training')})

    return render(request, 'club/booking_form.html', {'form': form})


@login_required
def cabinet(request):
    bookings = Booking.objects.filter(client=request.user)

    return render(request, 'club/cabinet.html', {'bookings': bookings})


@login_required
def admin_panel(request):
    if request.user.username != 'Admin':
        return redirect('home')

    bookings = Booking.objects.select_related('client', 'client__profile', 'training')

    return render(request, 'club/admin_panel.html', {'bookings': bookings})


@login_required
def change_status(request, pk):
    if request.user.username != 'Admin':
        return redirect('home')

    booking = get_object_or_404(Booking, pk=pk)
    booking.status = request.POST.get('status')
    booking.save()

    return redirect('admin_panel')
