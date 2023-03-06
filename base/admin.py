from django.contrib import admin

# Register your models here.

from .models import Room, Topic, Message#kazvame koi migracii iskame da se dobavqt kum admin panela

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)