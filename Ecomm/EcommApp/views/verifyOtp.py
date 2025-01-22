from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages  # Import messages framework

otp_storage = {}

class VeryfyOTP(View):
    def get(self, request):
        return render(request, 'verify_otp.html')
    
    def post(self, request):
        email = request.session.get('email')  # Retrieve email from session

        if not email:
            # If the email is not found in session, redirect to forget password page
            messages.error(request, "Session expired. Please request OTP again.")
            return redirect('forget-password')
        
        try:
            otp_entered = int(request.POST.get('otp'))
        except (ValueError, TypeError):
            messages.error(request, "Invalid OTP format. Please enter a numeric OTP.")
            return redirect('verify-otp')

        stored_otp = request.session.get('otp')

        print(f"OTP entered: {otp_entered}")  # Debugging line
        print(f"Session email: {email}")  # Debugging line
        print(f"Stored OTP from session: {stored_otp}") 

        if stored_otp == otp_entered:
            messages.success(request, "OTP verified successfully! Please reset your password.")
            return redirect('/reset-password')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify-otp')
