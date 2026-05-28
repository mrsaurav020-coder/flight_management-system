from django.contrib.auth.models import User
from urllib import request

from .models import Flight, Booking
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):

    source = request.GET.get('source')

    destination = request.GET.get('destination')

    flights = Flight.objects.all()

    if source and destination:

        flights = Flight.objects.filter(
            source__icontains=source,
            destination__icontains=destination
        )

    context = {

        'flights': flights

    }

    return render(request,
                  'home.html',
                  context)

def book_flight(request, id):

    if not request.user.is_authenticated:

        messages.error(
            request,
            "Please login before booking flights."
        )

        return redirect('/login/')

    flight = get_object_or_404(Flight, id=id)

    if request.method == "POST":

        if flight.available_seats <= 0:
            messages.error(
                request,
                "Flight is full."
            )
            return redirect('/')

        passenger_name = request.POST['passenger_name']

        passenger_email = request.POST['passenger_email']

        Booking.objects.create(

            user=request.user,

            passenger_name=passenger_name,

            passenger_email=passenger_email,

            flight=flight
        )
        flight.available_seats -= 1
        flight.save()

        return redirect('/history/')

    return render(request,
                  'book.html',
                  {'flight': flight})

def user_login(request):

    if request.method == "POST":

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            next_url = request.GET.get('next', '/')

            return redirect(next_url)

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(request, 'login.html')

def register(request):

    if request.method == "POST":

        username = request.POST['username']

        email = request.POST['email']

        password = request.POST['password']

        # CHECK IF USERNAME EXISTS

        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect('/register/')

        # CREATE USER

        User.objects.create_user(

            username=username,

            email=email,

            password=password
        )

        messages.success(
            request,
            "Account created successfully."
        )

        return redirect('/login/')

    return render(request, 'register.html')

@login_required
def history(request):

    bookings = Booking.objects.filter(user=request.user)

    return render(
        request,
        'history.html',
        {'bookings': bookings}
    )

def user_logout(request):
    logout(request)
    return redirect('/login/')
