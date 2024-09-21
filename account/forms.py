# account/forms.py
from django import forms
from .models import CustomUser
from .models import UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password

    class LoginForm(forms.Form):
        email = forms.EmailField()
        password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=255,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }),
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.'
        }
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        }),
        error_messages={
            'required': 'Password is required.'
        }
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'weight',
            'height',
            'region',
            'province',
            'municipality',
            'blood_type',
            'availability',
            'last_donation_date'
        ]

    # Optional: Add custom validation if needed
    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight <= 0:
            raise forms.ValidationError("Weight must be a positive number.")
        return weight

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height <= 0:
            raise forms.ValidationError("Height must be a positive number.")
        return height