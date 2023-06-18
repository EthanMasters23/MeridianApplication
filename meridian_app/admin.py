from django.contrib import admin
from .models import ClockIn
from .models import ContactForm

class ClockInAdmin(admin.ModelAdmin):
    list_display = ('employee', 'time_punches')

admin.site.register(ClockIn, ClockInAdmin)

admin.site.register(ContactForm)