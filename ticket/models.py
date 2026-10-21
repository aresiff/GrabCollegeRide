# Create your models here.

from django.db import models
import uuid

# Create your models here.

class Student(models.Model):
    studentid=models.CharField(max_length=10, primary_key=True)
    studentname=models.TextField(max_length=100)
    studentphoneno=models.TextField(max_length=100)
    studentaddress=models.TextField(max_length=100)
    studentpass=models.TextField(max_length=100)

class Driver(models.Model):
    driverid=models.CharField(max_length=10, primary_key=True)
    drivername=models.TextField(max_length=100)
    driverphoneno=models.TextField(max_length=100)
    driverpass=models.TextField(max_length=100)
    vehicleplateno=models.TextField(max_length=100)
    vehiclebrand=models.TextField(max_length=100)
    vehicletype=models.TextField(max_length=100)
    vehiclecapacity=models.IntegerField()
    
class Routefrom(models.Model):
    routefromid=models.CharField(max_length=10, primary_key=True)
    routefromname=models.TextField(max_length=100)

class Routeto(models.Model):
    routetoid=models.CharField(max_length=10, primary_key=True)
    routetoname=models.TextField(max_length=100)

class Booking(models.Model):
    bookingid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    studentid=models.ForeignKey(Student, on_delete=models.CASCADE)
    personcapacity=models.ForeignKey(Driver, on_delete=models.CASCADE)
    bookingtime=models.DateTimeField()
    pickup_time=models.DateTimeField()
    routefrom=models.ForeignKey(Routefrom, on_delete=models.CASCADE)
    routeto=models.ForeignKey(Routeto, on_delete=models.CASCADE)  