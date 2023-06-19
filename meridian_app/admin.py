from django.contrib import admin
from .models import ClockIn, Contact 
from .models import Contact 

class ClockInAdmin(admin.ModelAdmin):
    list_display = ('employee', 'time_punches')

admin.site.register(ClockIn, ClockInAdmin)

# admin.site.register(Contact)


