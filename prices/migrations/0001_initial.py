# Generated by Django 5.1.6 on 2025-03-03 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FruitPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('fruit_name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('unit', models.CharField(choices=[('kg', 'Kg'), ('box', 'Box'), ('piece', 'Piece')], default='kg', max_length=6)),
            ],
            options={
                'unique_together': {('date', 'fruit_name')},
            },
        ),
    ]
