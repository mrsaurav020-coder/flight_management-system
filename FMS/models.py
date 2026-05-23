from django.db import models

class Flight(models.Model):
    flight_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    price = models.IntegerField()

    def __str__(self):
        return self.flight_name
    
class Booking(models.Model):
    passenger_name = models.CharField(max_length=100)
    passenger_email = models.EmailField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.passenger_name
