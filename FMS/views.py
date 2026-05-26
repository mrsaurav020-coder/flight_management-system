from urllib import request

from .models import Flight, Booking
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    flights = Flight.objects.all()
    return render(request, 'home.html', {'flights': flights})

def book_flight(request, id):

    if not request.user.is_authenticated:

        messages.error(
            request,
            "Please login before booking flights."
        )

        return redirect('/login/')

    flight = get_object_or_404(Flight, id=id)

    if request.method == "POST":

        passenger_name = request.POST['passenger_name']

        passenger_email = request.POST['passenger_email']

        Booking.objects.create(

            user=request.user,

            passenger_name=passenger_name,

            passenger_email=passenger_email,

            flight=flight
        )

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
