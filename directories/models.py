from django.db import models

# Create your models here.
class Position(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Наименование')
    coefficient = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Тарифный коэффициент')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.name
    
class WorkSchedule(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Наименование')
    coefficient = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Коэффициент')

    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'Графики работы'

    def __str__(self):
        return self.name


class Competence(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Наименование')
    coefficient = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Коэффициент премии')

    class Meta:
        verbose_name = 'Компетенция'
        verbose_name_plural = 'Компетенции'

    def __str__(self):
        return self.name


class WorkCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Категория работ'
        verbose_name_plural = 'Категории работ'

    def __str__(self):
        return self.name


class OperationType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Тип операции'
        verbose_name_plural = 'Типы операций'

    def __str__(self):
        return self.name


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Наименование')

    class Meta:
        verbose_name = 'Категория расходов'
        verbose_name_plural = 'Категории расходов'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'

    def __str__(self):
        return self.name