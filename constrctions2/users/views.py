from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from users.forms import AdminUserCreationForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic import View
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.views import PasswordResetView

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user and log them in
            user = form.save()
            login(request, user)
            messages.success(request, "You have successfully registered and logged in.")
            return redirect('project_list')  # Or another redirect URL (e.g., the dashboard)
        else:
            # Print form errors for debugging
            print(form.errors)
            messages.error(request, "There is an error with your registration.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Get the user from the form and log them in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect('project_list')  # Redirect to the homepage or dashboard
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')  # Redirect to the login page after logout



def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Get email address from the form
            email = form.cleaned_data['email']
            
            # Check if the email exists in the database
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None
            
            if user:
                # Send password reset link to the email
                # You can adjust the link to be more specific to your application
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(user.pk.encode())
                domain = get_current_site(request).domain
                reset_link = f"http://{domain}/reset-password/{uid}/{token}/"
                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                send_mail(
                    'Password Reset',
                    message,
                    'noreply@yourdomain.com',
                    [email],
                )

            return redirect('password_reset_done')  # You can adjust this as per your need
    else:
        form = PasswordResetForm()
    return render(request, 'users/forgot_password.html', {'form': form})
from django.shortcuts import render

  # Render the admin dashboard page
def admin_dashboard(request):
    return render(request, 'bookings/admin_dashboard.html')

def admin_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# views.py

# views.py

class CustomPasswordResetView(PasswordResetView): # type: ignore
    template_name = 'password_reset_form.html'  # Custom template
    email_template_name = 'password_reset_email.html'  # Email template
    success_url = reverse_lazy('password_reset_done')