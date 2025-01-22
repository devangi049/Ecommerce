from django.shortcuts import render, redirect
from django.views import View
from EcommApp.models.user import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages  # Import messages framework

class ResetPassword(View):
    def get(self, request):
        return render(request, 'resetpassword.html')
    
    def post(self, request):
        new_password = request.POST.get('newPassword')
        confirm_new_password = request.POST.get('confirmNewPassword')

        if new_password == confirm_new_password:
            email = request.session.get('email')
            user = User.objects.filter(email=email).first()

            if user:
                hashed_password = make_password(new_password)
                user.password = hashed_password
                user.save()

                messages.success(request, "Password has been reset successfully! Please log in.")
                return redirect('login')
            else:
                messages.error(request, "User not found. Please try again.")
                return redirect('reset-password')
        else:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect('reset-password')
