from django.db import models

class FruitPrice(models.Model):
    UNIT_CHOICES = [
        ('kgs', 'Kilograms'),
        ('units', 'Units'),
        ('dozens', 'Dozens'),
    ]
    date = models.DateField()
    fruit_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=6, choices=UNIT_CHOICES, default='kgs')

    def __str__(self):
        return f"{self.fruit_name} - {self.date} ({self.unit})"

    class Meta:
        unique_together = ('date', 'fruit_name')  # Ensures uniqueness