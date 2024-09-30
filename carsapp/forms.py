from django import forms
from django.contrib.auth.hashers import make_password  # Import make_password
from .models import AssessorProfile
from django.core.exceptions import ValidationError

class AssessorProfileForm(forms.ModelForm):
    names = forms.CharField(max_length=255, help_text="Enter the assessor's full names.")
    id_number = forms.CharField(max_length=20, help_text="Enter a unique ID number.")
    username = forms.CharField(max_length=150, help_text="Enter a unique username.")
    password = forms.CharField(widget=forms.PasswordInput, help_text="Enter a secure password.")

    class Meta:
        model = AssessorProfile
        fields = ['names', 'id_number', 'username', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if AssessorProfile.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another one.")
        return username

    def save(self, commit=True):
        # Save the password securely
        profile = super().save(commit=False)
        profile.password = make_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            profile.save()
        return profile
