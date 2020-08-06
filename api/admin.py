from django.contrib import admin
from .models import Printer, Check


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    fields = ['name', 'check_type']
    ordering = ['name', 'check_type']


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    fields = ['printer', 'check_type', 'status']
    ordering = ['printer', 'check_type', 'status']
