from django.contrib import admin
from .models import Booking, Profile, Review, Training

admin.site.register(Profile)
admin.site.register(Training)
admin.site.register(Booking)
admin.site.register(Review)
