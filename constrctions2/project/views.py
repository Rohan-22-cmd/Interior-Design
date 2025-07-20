from django.shortcuts import render, get_object_or_404, redirect
from .models import ConstructionProject
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from .forms import ContactForm
from django.shortcuts import render
from .forms import ConsultationForm
from datetime import datetime, timedelta

# Project list view with search functionality
def project_list(request):
    query = request.GET.get('q', '')  # Get the search query from the GET request
    city = request.GET.get('city', '')  # Get the city filter from the GET request
    budget = request.GET.get('budget', '')  # Get the budget filter from the GET request
    
    # Start with all projects
    projects = ConstructionProject.objects.all()
    
    # Apply the search query filter if provided
    if query:
        projects = projects.filter(project_name__icontains=query)  # Case-insensitive search
    
    # Apply the city filter if provided
    if city:
        projects = projects.filter(location__icontains=city)  # Filter by city (location)
    
    # Apply the budget filter if provided
    if budget:
        try:
            budget_value = float(budget)  # Convert the budget to a float
            projects = projects.filter(budget__lte=budget_value)  # Filter by budget (less than or equal to)
        except ValueError:
            # Handle invalid budget value
            messages.error(request, "Please enter a valid numeric value for the budget.")
    
    # Return the filtered projects to the template
    return render(request, 'project/project_list.html', {
        'projects': projects,
        'query': query,
        'city': city,
        'budget': budget  # Pass all filter values to keep them in the form
    })
# Project details view, accessible only to logged-in users
@login_required
def project_details(request, pk):
    project = get_object_or_404(ConstructionProject, pk=pk)
    return render(request, 'project/project_details.html', {'project': project})

# About view
def about_view(request):
    return render(request, 'about.html')
def home1_view(request):
    return render(request, 'home1.html')
def home2_view(request):
    return render(request, 'home2.html')


# Contact view to handle form submission

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            user_name = form.cleaned_data['name']
            user_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Admin email (it could be fetched dynamically if needed)
            admin_email = settings.DEFAULT_FROM_EMAIL  # Or hard-code the admin email

            # Prepare the email content
            full_message = f"Message from {user_name} ({user_email}):\n\n{message}"

            # Send the email from the admin's email address to another email address (e.g., support email)
            send_mail(
                subject=f"Contact Form Submission: {subject}",
                message=full_message,
                from_email=admin_email,  # Email will appear from the admin
                recipient_list=['user_email'],  # Email recipient (replace with desired email)
                fail_silently=False,
            )
            

            # Optionally, redirect to a success page
            return redirect('thank_you')
    
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
def thank_you_view(request):
    return render(request, 'tahnkyou.html')
def informatin_you_view(request):
    return render(request, 'informatin.html')

def create_google_meet_event(start_time, end_time):
    # You would need the Google API and OAuth credentials here to create real Google Meet events
    return "https://meet.google.com/xyz-abc-def"  # Dummy link for now

# Zoom Meeting Link Generation (dummy function for now)
def create_zoom_meeting(start_time, duration):
    # Replace with your Zoom API call logic to create a meeting and get the link
    return "https://zoom.us/j/1234567890"  # Dummy link for now

# WhatsApp Link Generation (for consultation confirmation)
def create_whatsapp_link(phone_number, message):
    return f"https://wa.me/{phone_number}?text={message}"

def book_consultation(request):
    if request.method == "POST":
        form = ConsultationForm(request.POST)
        if form.is_valid():
            # Get user email and selected platform from the form
            user_email = form.cleaned_data['email']
            platform_choice = form.cleaned_data['platform_choice']
            meeting_name = 'Consultation Meeting'  # Static name for the meeting

            # Get start time and end time for the meeting (scheduled for 1 day from now)
            start_time = (datetime.utcnow() + timedelta(days=1))  # 1 day from now (UTC)
            end_time = start_time + timedelta(hours=1)  # 1-hour meeting duration

            # Convert start and end time to a string format to display in the email
            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')  # Format as YYYY-MM-DD HH:MM:SS
            end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')  # Format as YYYY-MM-DD HH:MM:SS

            # Based on the platform choice, generate the corresponding meeting link
            if platform_choice == 'google_meet':
                meeting_link = create_google_meet_event(start_time_str, end_time_str)  # Google Meet link
            elif platform_choice == 'zoom':
                meeting_link = create_zoom_meeting(start_time_str, 60)  # Zoom link (1-hour duration)
            elif platform_choice == 'whatsapp':
                meeting_link = create_whatsapp_link('1234567890', 'I would like to confirm my consultation')  # WhatsApp link

            # Create the email content with meeting time and link
            email_subject = f'Your {meeting_name} Booking'
            email_body = f"""
            Hello,

            Thank you for booking a {meeting_name}.

            Your meeting details are as follows:
            Meeting Name: {meeting_name}
            Meeting Date: {start_time_str}
            Meeting Time: {start_time_str} to {end_time_str}
            Meeting Link: {meeting_link}

            Please click the link above to join your consultation at the scheduled time.

            Best regards,
            Your Team
            """

            # Send the email to the user
            send_mail(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,  # Your "from" email address
                [user_email],  # Recipient's email address
                fail_silently=False,
            )

            # Render confirmation page after booking
            return render(request, 'project/booking_confirmation.html')  # Redirect to a confirmation page after booking

    else:
        form = ConsultationForm()

    return render(request, 'project/book_consultation.html', {'form': form})