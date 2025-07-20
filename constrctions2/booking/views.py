import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from project.models import ConstructionProject  # Assuming your project model is in the project app
from .models import Booking  # Booking model for construction projects
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
 # Assuming this is your project model
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
@login_required
def booking_now(request):
    """
    This view allows the user to start the booking process for a construction project.
    It multiplies the project budget by 100 and passes it to the template.
    """
    if request.method == 'POST':
        project_id = request.POST.get('project_id')  # Get the project ID from the POST request
        project = get_object_or_404(ConstructionProject, id=project_id)  # Fetch the project from DB

        # Multiply the budget by 100 (e.g., for currency conversion to paise)
        multiplied_price = project.budget * 100

        # Pass the project and multiplied price to the template
        return render(request, 'bookings/booking_form.html', {
            'project': project,
            'multiplied_price': multiplied_price
        })

    return render(request, 'bookings/booking_form.html')


from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
# Assuming ConstructionProject is imported correctly

# In your booking_submit view:
from django.conf import settings
import razorpay

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))

# views.py
import razorpay
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import BookingForm
from .models import Booking

import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

import hashlib
import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
import razorpay

# Razorpay client setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

@login_required
def booking_submit(request):
    if request.method == 'POST':
        try:
            # Get the project ID and fetch the project details
            project_id = request.POST.get('project_id')
            project = get_object_or_404(ConstructionProject, id=project_id)
            
            # Multiply the budget by 100 to convert to paise (INR to paise)
            multiplied_price = project.budget * 100  # In paise (100 paise = 1 INR)

            # Halve the price for the payment (i.e., take 50% of the total amount)
            first_instrument_amount = multiplied_price / 2  # First instrument (half)
            second_instrument_amount = multiplied_price / 2  # Second instrument (second half)

            # Step 2: Create Razorpay order
            amount_in_paise = int(first_instrument_amount)  # Razorpay expects the amount to be in paise (integer)
            order_data = {
                "amount": amount_in_paise,  # Amount in paise
                "currency": "INR",
                "payment_capture": "1",  # Auto capture on success
            }

            # Create the Razorpay order
            order = razorpay_client.order.create(dict(order_data))
            razorpay_order_id = order['id']

            # Save the Razorpay order ID and the first and second instrument amounts in the booking model
            booking = Booking.objects.create(
                project=project,
                name=request.POST.get('name'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                budget=project.budget,
                payment_status='pending',  # Payment status is 'pending' initially
                razorpay_order_id=razorpay_order_id,  # Store the order ID in the booking
                first_instrument_amount=first_instrument_amount / 100,  # Store the first instrument amount (convert paise to INR)
                second_instrument_amount=second_instrument_amount / 100,  # Store the second instrument amount (convert paise to INR)
                user=request.user  # Assign the logged-in user to the booking
            )

            # Return the Razorpay order ID to the template for payment
            return render(request, 'bookings/booking_form.html', {
                'razorpay_order_id': razorpay_order_id,
                'multiplied_price': multiplied_price / 100,  # Convert back to INR for display
                'project': project,
                'booking_id': booking.id,  # Pass the booking ID to track the booking
            })

        except Exception as e:
            return HttpResponse(f"An unexpected error occurred: {str(e)}", status=500)
@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        secret = settings.RAZORPAY_API_SECRET
        string = f'{order_id}|{payment_id}'
        expected_signature = hashlib.sha256(string.encode('utf-8')).hexdigest()

        if signature == expected_signature:
            booking = Booking.objects.get(razorpay_order_id=order_id)

            if booking.payment_status != 'completed':
                # First payment successful, mark it as completed and enable the second payment
                booking.payment_status = 'completed'
                booking.partial_payment_amount = booking.first_instrument_amount
                booking.save()

                # If you want to proceed with the second payment, you can handle it later
                return HttpResponse('Payment successful.')
        else:
            booking = Booking.objects.get(razorpay_order_id=order_id)
            booking.payment_status = 'failed'
            booking.save()
            return HttpResponse('Payment verification failed.')

    return HttpResponseForbidden("Invalid request method.")


from django.shortcuts import render
from django.db.models import Q
from .models import Booking
from decimal import Decimal, InvalidOperation
# views.py
from django.db.models import Q

def admin_dashboard1(request):
    search_query = request.GET.get('search_query', '')
    payment_status_query = request.GET.get('payment_status', '')
    bookings = Booking.objects.all()

    if search_query:
        try:
            if search_query.replace('.', '', 1).isdigit():
                budget_value = Decimal(search_query)
                bookings = bookings.filter(budget=budget_value)
            else:
                bookings = bookings.filter(
                    Q(project__project_name__icontains=search_query) |
                    Q(name__icontains=search_query)
                )
        except InvalidOperation:
            pass

    if payment_status_query:
        bookings = bookings.filter(payment_status=payment_status_query)

    # Calculate total payment and remaining balance for each booking
    for booking in bookings:
        total_payment = booking.partial_payment_amount + booking.second_instrument_amount
        remaining_balance = booking.budget - total_payment
        booking.total_payment = total_payment
        booking.remaining_balance = remaining_balance

    return render(request, 'bookings/admin_dashboard.html', {
        'bookings': bookings,
        'search_query': search_query,
        'payment_status_query': payment_status_query,
    })
