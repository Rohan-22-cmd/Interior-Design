
# forms.py
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'project', 'name', 'address', 'phone', 'budget', 'payment_status', 'razorpay_order_id', 'other_field']

    # Optionally, you can add custom validation or widgets
    def clean_razorpay_order_id(self):
        razorpay_order_id = self.cleaned_data.get('razorpay_order_id')
        if not razorpay_order_id:
            raise forms.ValidationError("Razorpay Order ID is required.")
        return razorpay_order_id

    def clean_other_field(self):
        other_field = self.cleaned_data.get('other_field')
        if not other_field:
            raise forms.ValidationError("Other field is required.")
        return other_field
