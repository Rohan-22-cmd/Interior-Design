# Generated by Django 5.1.3 on 2025-03-12 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_booking_partial_payment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='first_instrument_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='booking',
            name='second_instrument_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
