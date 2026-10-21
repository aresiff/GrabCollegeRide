from django.contrib import admin

from ticket.models import Student, Driver, Routefrom, Routeto, Booking

# Register your models here.

admin.site.register(Student)
admin.site.register(Driver)
admin.site.register(Routefrom)
admin.site.register(Routeto)
admin.site.register(Booking)