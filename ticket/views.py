from django.shortcuts import render, redirect, get_object_or_404
from ticket.models import Student
from ticket.models import Driver
from ticket.models import Routefrom
from ticket.models import Routeto
from ticket.models import Booking
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.contrib import messages


# Create your views here.

def index(request): 
    myStudent = Student.objects.all().values()
    myDriver = Driver.objects.all().values()
    context={
        'myStudent': myStudent,
        'myDriver': myDriver, 
    }
    return render(request, 'index.html', context)

def studentlogin(request):
    if request.method == 'POST':
        # Get the student ID and password from the form
        student_id = request.POST['student_id']
        student_password = request.POST['password']

        # Check if the student with the entered ID exists
        try:
            student = Student.objects.get(studentid=student_id)
            
        except Student.DoesNotExist:
            context = {
                'message': 'Invalid student ID or password. Please try again.'
            }
            return render(request, 'studentlogin.html', context)

        # Verify if the entered password matches the student’s password
        if student.studentpass == student_password:
            context = {
                'message': 'Login successful!',
                'student_name': student.studentname
            }
            request.session['studentid'] = student_id  # Save student ID to session      
            return redirect('studenthomepage')  # Redirect to the student's dashboard or home page
        else:
            context = {
                'message': 'Invalid student ID or password. Please try again.'
            }
            return render(request, 'studentlogin.html', context)

    # If it's not a POST request, render the login page
    return render(request, 'studentlogin.html')


def studentsignup(request):
    displaydata = Student.objects.all().values()
    if request.method == 'POST':
        studentid1 = request.POST['studentid']
        studentname1 = request.POST['studentname']
        studentphoneno1 = request.POST['studentphoneno']
        studentaddress1 = request.POST['studentaddress']
        studentpass1 = request.POST['studentpass']
        data = Student(studentid=studentid1, studentname=studentname1, studentphoneno=studentphoneno1, studentaddress=studentaddress1, studentpass=studentpass1)
        data.save()

        return redirect('studentlogin')
    else:
        dict = {
            'message':'',
            'displaydata':displaydata,

        }
    return render(request, 'studentsignup.html', dict)


def driverlogin(request):
    if request.method == 'POST':
        # Get the driver ID and password from the form
        driver_id = request.POST['driver_id']
        driver_password = request.POST['password']

        # Check if the driver with the entered ID exists
        try:
            driver = Driver.objects.get(driverid=driver_id)
        except Driver.DoesNotExist:
            context = {
                'message': 'Invalid driver ID or password. Please try again.'
            }
            return render(request, 'driverlogin.html', context)

        # Verify if the entered password matches the driver’s password
        if driver.driverpass == driver_password:
            context = {
                'message': 'Login successful!',
                'student_name': driver.drivername
            }
            # Store the driver ID in the session
            request.session['driverid'] = driver.driverid
            return redirect('driverhomepage')  # Redirect to the driver's dashboard or home page
        else:
            context = {
                'message': 'Invalid student ID or password. Please try again.'
            }
            return render(request, 'driverlogin.html', context)

    # If it's not a POST request, render the login page
    return render(request, 'driverlogin.html')


def driversignup(request):
    displaydata = Driver.objects.all().values()
    if request.method == 'POST':
        driverid1 = request.POST['driverid']
        drivername1 = request.POST['drivername']
        driverphoneno1 = request.POST['driverphoneno']
        driverpass1 = request.POST['driverpass']
        vehicleplateno1 = request.POST['vehicleplateno']
        vehiclebrand1 = request.POST['vehiclebrand']
        vehicletype1 = request.POST['vehicletype']
        vehiclecapacity1 = request.POST['vehiclecapacity']
        data = Driver(driverid=driverid1, drivername=drivername1, driverphoneno=driverphoneno1, driverpass=driverpass1, vehicleplateno=vehicleplateno1, vehiclebrand=vehiclebrand1, vehicletype=vehicletype1, vehiclecapacity=vehiclecapacity1)
        data.save()

        return redirect('driverlogin')
    else:
        dict = {
            'message':'',
            'displaydata':displaydata,

        }
    return render(request, 'driversignup.html', dict)


def studenthomepage(request):
    student = Student.objects.get(studentid=request.session['studentid'])
    return render(request, 'studenthomepage.html', {'studentname': student.studentname})

def driverhomepage(request):
    # Get the currently logged-in driver's ID from the session
    driverid = request.session.get('driverid')

    # Fetch the driver details from the database
    driver = Driver.objects.get(driverid=driverid)

    # Pass the driver's name to the template
    return render(request, 'driverhomepage.html', {'drivername': driver.drivername})


def student_booking(request):
    # Get the logged-in student
    student = Student.objects.get(studentid=request.session['studentid'])  # Assuming studentid is stored in session after login
    
    # Fetch route options and drivers
    routefrom_list = Routefrom.objects.all()
    routeto_list = Routeto.objects.all()
    drivers_list = Driver.objects.all()

    if request.method == 'POST':
        # Get the submitted form data
        routefrom_id = request.POST['routefrom']
        routeto_id = request.POST['routeto']
        driver_id = request.POST['driver']
        person_capacity = int(request.POST['personcapacity'])
        pickup_time = request.POST['pickup_time']

        # Get driver and validate capacity
        driver = Driver.objects.get(driverid=driver_id)
        if person_capacity > driver.vehiclecapacity:
            return HttpResponse("Error: Number of people exceeds the vehicle's capacity.")
        
        # Create a new booking
        booking = Booking(
            studentid=student,
            personcapacity=driver,  # Driver associated with booking capacity
            bookingtime=timezone.now(),
            pickup_time=pickup_time,
            routefrom=Routefrom.objects.get(routefromid=routefrom_id),
            routeto=Routeto.objects.get(routetoid=routeto_id)
        )
        booking.save()

        # Redirect to booking confirmation page
        return redirect('studentbookingconfirmed')

    # Render the booking form page
    context = {
        'student': student,
        'routefrom': routefrom_list,
        'routeto': routeto_list,
        'drivers': drivers_list
    }
    return render(request, 'studentbooking.html', context)


def student_booking_confirmed(request):
    return render(request, 'studentbookingconfirmed.html')



def booking_history(request):
    # Get the logged-in student's ID from session
    student = Student.objects.get(studentid=request.session['studentid'])

    # Fetch all bookings for the logged-in student
    bookings = Booking.objects.filter(studentid=student)

    context = {
        'bookings': bookings
    }
    return render(request, 'studenthistory.html', context)

def cancel_booking(request, booking_id):
    # Get the booking by ID and delete it
    booking = get_object_or_404(Booking, bookingid=booking_id)
    booking.delete()

    # Redirect back to booking history page after deletion
    return redirect('studenthistory')

def update_booking_page(request, booking_id):
    booking = get_object_or_404(Booking, bookingid=booking_id)

    # Fetch data for route options and drivers (same as in booking page)
    routefrom_list = Routefrom.objects.all()
    routeto_list = Routeto.objects.all()
    drivers_list = Driver.objects.all()

    if request.method == 'POST':
        # Get updated booking data
        routefrom_id = request.POST['routefrom']
        routeto_id = request.POST['routeto']
        driver_id = request.POST['driver']
        person_capacity = int(request.POST['personcapacity'])
        pickup_time = request.POST['pickup_time']

        # Validate driver capacity
        driver = Driver.objects.get(driverid=driver_id)
        if person_capacity > driver.vehiclecapacity:
            return HttpResponse("Error: Number of people exceeds the vehicle's capacity.")
            

        # Update booking details
        booking.routefrom = Routefrom.objects.get(routefromid=routefrom_id)
        booking.routeto = Routeto.objects.get(routetoid=routeto_id)
        booking.personcapacity = driver
        booking.pickup_time = pickup_time
        booking.save()

        # Redirect to history page after updating
        return redirect('studenthistory')

    context = {
        'booking': booking,
        'routefrom': routefrom_list,
        'routeto': routeto_list,
        'drivers': drivers_list
    }
    return render(request, 'update_booking_page.html', context)


def driver_booking_list(request):
    # Check if the driver ID is stored in the session
    driverid = request.session.get('driverid')

    if not driverid:
        # Redirect to the login page if the driver is not logged in
        return redirect('driverlogin')

    # Get the currently logged-in driver using the session driverid
    current_driver = Driver.objects.get(driverid=driverid)

    # Filter bookings based on the signed-in driver
    bookings = Booking.objects.filter(personcapacity=current_driver)

    # Pass the bookings to the template
    context = {
        'bookings': bookings
    }
    return render(request, 'driver_booking_list.html', context)

def driver_cancel_booking(request, booking_id):
    # Check if the driver ID is stored in the session
    driverid = request.session.get('driverid')

    if not driverid:
        # Redirect to the login page if the driver is not logged in
        return redirect('driverlogin')

    # Get the currently logged-in driver using the session driverid
    current_driver = Driver.objects.get(driverid=driverid)

    # Get the booking object and ensure it belongs to the logged-in driver
    booking = get_object_or_404(Booking, bookingid=booking_id, personcapacity=current_driver)

    # Delete the booking
    booking.delete()

    # Redirect back to the driver booking list page after deletion
    return redirect('driver_booking_list')

def search_bookings(request):
    # Check if the driver ID is stored in the session
    driverid = request.session.get('driverid')

    if not driverid:
        # Redirect to the login page if the driver is not logged in
        return redirect('driverlogin')

    # Render the search page where the driver can input a date
    return render(request, 'search_bookings.html')


def booking_search_results(request):
    # Check if the driver ID is stored in the session
    driverid = request.session.get('driverid')

    if not driverid:
        # Redirect to the login page if the driver is not logged in
        return redirect('driverlogin')

    # Get the currently logged-in driver using the session driverid
    current_driver = Driver.objects.get(driverid=driverid)

    # Get the search date from the GET parameters
    search_date = request.GET.get('search_date')

    # Initialize bookings to empty initially
    bookings = []

    if search_date:
        # Parse the search date and filter bookings based on pickup_time
        try:
            search_date_parsed = parse_date(search_date)
            bookings = Booking.objects.filter(personcapacity=current_driver, pickup_time__date=search_date_parsed)
        except ValueError:
            bookings = []

    # Pass the bookings and the search query to the template
    context = {
        'bookings': bookings,
        'search_date': search_date
    }
    return render(request, 'booking_search_results.html', context)



def driver_profile(request):
    driverid = request.session.get('driverid')

    if not driverid:
        return redirect('driverlogin')

    driver = get_object_or_404(Driver, driverid=driverid)

    if request.method == 'POST':
        # Update driver information
        driver_name = request.POST.get('drivername')
        driver_phone = request.POST.get('driverphoneno')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Update driver fields
        if driver_name:
            driver.drivername = driver_name
        if driver_phone:
            driver.driverphoneno = driver_phone

        # Handle password change
        if new_password and confirm_password:
            if current_password == driver.driverpass:
                if new_password == confirm_password:
                    driver.driverpass = new_password
                    messages.success(request, 'Your profile and password have been updated successfully!')
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                messages.error(request, 'Current password is incorrect.')

        driver.save()
        messages.success(request, 'Your profile has been updated successfully!')

    return render(request, 'driver_profile.html', {'driver': driver})

def student_profile(request):
    studentid = request.session.get('studentid')

    if not studentid:
        return redirect('studentlogin')

    student = get_object_or_404(Student, studentid=studentid)

    if request.method == 'POST':
        # Update driver information
        student_name = request.POST.get('studentname')
        student_phone = request.POST.get('studentphoneno')
        student_address = request.POST.get('studentaddress')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Update driver fields
        if student_name:
            student.studentname = student_name
        if student_phone:
            student.studentphoneno = student_phone
        if student_address:
            student.studentaddress = student_address

        # Handle password change
        if new_password and confirm_password:
            if current_password == student.studentpass:
                if new_password == confirm_password:
                    student.studentpass = new_password
                    messages.success(request, 'Your profile and password have been updated successfully!')
                else:
                    messages.error(request, 'New passwords do not match.')
            else:
                messages.error(request, 'Current password is incorrect.')

        student.save()
        messages.success(request, 'Your profile has been updated successfully!')

    return render(request, 'student_profile.html', {'student': student})





