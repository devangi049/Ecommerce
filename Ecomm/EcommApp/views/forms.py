from django import forms
from EcommApp.models.contact import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'website', 'message']
