from django.db import models
from django.conf import settings

class Booking(models.Model):
    PENDING = 'PENDING'
    PAID = 'PAID'
    FAILED = 'FAILED'

    PAYMENT_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PAID, 'Paid'),
        (FAILED, 'Failed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey('project.ConstructionProject', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # Client's name
    address = models.TextField()
    phone = models.CharField(max_length=20)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    partial_payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)  # Store Razorpay order ID
    other_field = models.CharField(max_length=255, blank=True, null=True)  # Example for another custom field

    # New fields for the first and second instrument amounts
    first_instrument_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Amount for first instrument
    second_instrument_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Amount for second instrument

    def __str__(self):
        return f"{self.user.username} - {self.project.project_name} ({self.payment_status})"
