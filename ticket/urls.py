from django.urls import path
from . import views

urlpatterns =[
    path("", views.index, name = "index"),
    path("studentlogin", views.studentlogin, name = "studentlogin"),
    path("studentsignup", views.studentsignup, name = "studentsignup"),
    path("driverlogin", views.driverlogin, name = "driverlogin"),
    path("driversignup", views.driversignup, name = "driversignup"),
    path("studenthomepage/", views.studenthomepage, name = "studenthomepage"),
    path("driverhomepage/", views.driverhomepage, name = "driverhomepage"),
    path('studenthomepage/booking/', views.student_booking, name='student_booking'),
    path('booking-confirmed/', views.student_booking_confirmed, name='studentbookingconfirmed'),
    path('bookinghistory/', views.booking_history, name='studenthistory'),
    path('cancelbooking/<str:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('updatebooking/<str:booking_id>/', views.update_booking_page, name='update_booking_page'),
    path('driver/login/', views.driverlogin, name='driverlogin'),
    path('driver/bookings/', views.driver_booking_list, name='driver_booking_list'),
    path('driver/bookings/cancel/<uuid:booking_id>/', views.driver_cancel_booking, name='driver_cancel_booking'), 
    path('driver/homepage/', views.driverhomepage, name='driverhomepage'),
    path('driver/search/', views.search_bookings, name='search_bookings'),
    path('driver/search/results/', views.booking_search_results, name='booking_search_results'),
    path('driver/profile/', views.driver_profile, name='driver_profile'),
    path('student/profile/', views.student_profile, name='student_profile'),
     
]