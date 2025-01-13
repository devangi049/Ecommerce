from django.shortcuts import render, redirect
from django.core.mail import send_mail
from EcommApp.models.contact import Contact
from .forms import ContactForm
from django.conf import settings
from django.contrib import messages

def Contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save contact message to the database
            form.save()

            
            
            # Show success message and redirect
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Assuming the URL is named 'contact'
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
