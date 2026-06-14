from django.contrib import admin

# Register your models here.
from .models import Position

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'coefficient')