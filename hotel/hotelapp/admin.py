from django.contrib import admin
from .models import ownermodel, roommodel, hotelmodel
# Register your models here.
admin.site.register(hotelmodel)
admin.site.register(ownermodel)
admin.site.register(roommodel)