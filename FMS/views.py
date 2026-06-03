from django.contrib.auth.models import User
from urllib import request
from django.http import HttpResponse
from reportlab.pdfgen import canvas
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
        travel_date = request.POST['travel_date']
        request.session['flight_id'] = flight.id
        request.session['passenger_name'] = passenger_name
        request.session['passenger_email'] = passenger_email
        request.session['travel_date'] = travel_date
        return redirect('payment')

    #     booking = Booking.objects.create(
    #         user=request.user,
    #         passenger_name=passenger_name,
    #         passenger_email=passenger_email,
    #         travel_date=travel_date,
    #         flight=flight
    #     )
    #     flight.available_seats -= 1
    #     flight.save()
    #     return redirect(f'/success/{booking.id}/')    
    return render(request,'book.html',{'flight': flight})

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

def signup(request):
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
            return redirect('/signup/')
        

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
    return render(request, 'signup.html')

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

def success(request, id):
    booking = get_object_or_404(
        Booking,
        id=id
    )
    return render(
        request,
        'success.html',
        {'booking': booking}
    )

def download_ticket(request, id):
    booking = get_object_or_404(
        Booking,
        id=id
    )
    response = HttpResponse(
        content_type='application/pdf'
    )
    response['Content-Disposition'] = (
        f'attachment; filename="ticket_{booking.id}.pdf"'
    )
    p = canvas.Canvas(response)

    # TITLE
    p.setFont("Helvetica-Bold", 28)
    p.setFillColorRGB(0, 0.4, 0.9)
    p.drawString(
        170,
        820,
        "SkyConnect"
    )
    p.setFillColorRGB(0,0,0)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(
        180,
        780,
        "Flight Ticket"
    )

    # TICKET DETAILS
    p.setFont("Helvetica", 14)
    p.drawString(
        100,
        740,
        f"Ticket ID: Sky{booking.id}2025"
    )
    p.drawString(
        100,
        700,
        f"Passenger: {booking.passenger_name}"
    )
    p.drawString(
        100,
        660,
        f"Email: {booking.passenger_email}"
    )
    p.drawString(
        100,
        620,
        f"Flight: {booking.flight.flight_name}"
    )
    p.drawString(
        100,
        580,
        f"Route: {booking.flight.source} to {booking.flight.destination}"
    )
    p.drawString(
        100,
        540,
        f"Departure: {booking.flight.departure_time}"
    )
    p.drawString(
        100,
        500,
        f"Arrival: {booking.flight.arrival_time}"
    )
    p.drawString(
        100,
        460,
        f"Travel Date: {booking.travel_date}"
    )
    p.drawString(
        100,
        420,
        f"Price: Rs.{booking.flight.price}"
    )
    p.setFillColorRGB(0, 0.5, 1)
    p.drawString(
        100,
        360,
        "Thank you for choosing SkyConnect"
    )
    p.setFillColorRGB(0, 0, 0)
    p.showPage()
    p.save()

    return response

def payment(request):

    flight_id = request.session.get('flight_id')
    flight = Flight.objects.get(id=flight_id)
    if request.method == "POST":
        passenger_name = request.session.get('passenger_name')
        passenger_email = request.session.get('passenger_email')
        travel_date = request.session.get('travel_date')
        
        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            passenger_name=passenger_name,
            passenger_email=passenger_email,
            travel_date=travel_date
        )
        flight.available_seats -= 1
        flight.save()
        return redirect(f'/success/{booking.id}/')
    return render(request, 'payment.html', {'flight': flight})

def cancel_booking(request, id):
    booking = Booking.objects.get(id=id)
    if booking.status == "Confirmed":
        booking.status = "Cancelled"
        booking.save()
        booking.flight.available_seats += 1
        booking.flight.save()
    return redirect('history')