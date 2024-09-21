# account/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, UserProfileForm, RegistrationForm
from .models import UserProfile, BloodDonationRequest
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils import timezone

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                # Check if the user has a profile
                try:
                    profile = UserProfile.objects.get(user=user)
                    login(request, user)  # Log the user in
                    return redirect('home')  # Redirect to homepage if profile exists
                except UserProfile.DoesNotExist:
                    messages.warning(request, "Please complete your profile.")
                    return redirect('complete_profile')  # Redirect to profile completion page

            messages.error(request, "Invalid credentials.")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def complete_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile_data = form.save(commit=False)
            profile_data.user = request.user  # Link profile to logged-in user
            profile_data.save()
            messages.success(request, "Profile completed successfully!")
            return redirect('home')

    else:
        form = UserProfileForm()

    return render(request, 'complete_profile.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the new user instance
            user = form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()  # Create an empty form instance

    return render(request, 'register.html', {'form': form})

class UpdateProfileView(View):
    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        form = UserProfileForm(instance=user_profile)  # Pre-fill form with current data
        return render(request, 'update_profile.html', {'form': form})

    def post(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        form = UserProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            # Check availability logic
            new_availability = form.cleaned_data['availability']
            last_donation_date = user_profile.last_donation_date

            if new_availability and last_donation_date:
                days_since_last_donation = (timezone.now().date() - last_donation_date).days

                if days_since_last_donation < 56:
                    days_remaining = 56 - days_since_last_donation
                    form.add_error('availability',
                                   f"You must wait {days_remaining} more days before becoming available again.")
                    return render(request, 'update_profile.html', {'form': form})

            # Save updated profile data (excluding blood type)
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to profile view after updating

        return render(request, 'update_profile.html', {'form': form})

@login_required
def profile_view(request):
    # Get the user's profile
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Get all blood donation requests made by the user
    blood_donations = BloodDonationRequest.objects.filter(donor=request.user)  # Assuming you have a donor field

    context = {
        'user_profile': user_profile,
        'blood_donations': blood_donations,
    }

    return render(request, 'profile.html', context)