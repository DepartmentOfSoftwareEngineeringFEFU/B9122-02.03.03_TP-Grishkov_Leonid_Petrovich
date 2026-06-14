from django.contrib import admin

# Register your models here.
from .models import Position, WorkSchedule, Competence, WorkCategory, OperationType, ExpenseCategory, Product

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'coefficient')

@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'coefficient')

@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'coefficient')

@admin.register(WorkCategory)
class WorkCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(OperationType)
class OperationTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')