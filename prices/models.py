from django.db import models

class FruitPrice(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kg'),
        ('box', 'Box'),
        ('piece', 'Piece'),
    ]
    date = models.DateField()
    fruit_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)  # Increased to 99,999.99
    unit = models.CharField(max_length=6, choices=UNIT_CHOICES, default='kg')

    def __str__(self):
        return f"{self.fruit_name} - {self.date} ({self.unit})"

    class Meta:
        unique_together = ('date', 'fruit_name')