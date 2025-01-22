from django.shortcuts import render, redirect
from django.views import View
from EcommApp.models.user import User
import random
from django.core.mail import send_mail
from django.contrib import messages  # Import messages framework

otp_storage = {}

class ForgetPassword(View):
    def get(self, request):
        return render(request, 'forgetpassword.html')

    def post(self, request):
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            otp = random.randint(100000, 999999)
            otp_storage[email] = otp
            print(f"OTP stored for {email}: {otp}")  # Debugging line

            # Store email and OTP in session
            request.session['otp'] = otp
            request.session['email'] = email
            request.session.save()

            # Send OTP email
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is: {otp}',
                'from@example.com',  # Replace with your sender email
                [email],
                fail_silently=False,
            )

            # Add success message
            messages.success(request, "An OTP has been sent to your email address.")
            return redirect('/verify-otp')
        else:
            # Add error message
            messages.error(request, "Email does not exist.")
            return render(request, 'forgetpassword.html')
