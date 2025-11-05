# forms.py
from django import forms
from .models import Contact, Booking, Puja, Priest, Epass
from django.utils import timezone


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your message...'}),
        }


class PujaBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['puja', 'priest', 'user_name','user_email',  'user_phone', 'date', 'time']


        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }        

        
class EpassForm(forms.ModelForm):
    class Meta:
        model = Epass
        fields = ['name', 'number_of_people', 'date_of_visit', 'contact_number', 'email', 'purpose']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'number_of_people': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of People'}),
            'date_of_visit': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'contact_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter the purpose of visit'}),
        }
        