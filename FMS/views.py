from .models import Flight, Booking
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def home(request):
    flights = Flight.objects.all()
    return render(request, 'home.html', {'flights': flights})

@login_required

def book_flight(request, id):

    flight = get_object_or_404(Flight, id=id)

    if request.method == "POST":

        passenger_name = request.POST['passenger_name']

        passenger_email = request.POST['passenger_email']

        Booking.objects.create(

            passenger_name=passenger_name,

            passenger_email=passenger_email,

            flight=flight
        )

    return render(request, 'book.html', {'flight': flight})

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

            return redirect('/')

    return render(request, 'login.html')
