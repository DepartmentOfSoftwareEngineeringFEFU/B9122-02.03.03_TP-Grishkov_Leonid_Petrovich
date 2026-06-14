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