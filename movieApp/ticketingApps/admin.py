from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Theater)
admin.site.register(Profile)
admin.site.register(Movie)
admin.site.register(Order)
admin.site.register(Room)
admin.site.register(Movieshowing)
admin.site.register(Seatsbought)

