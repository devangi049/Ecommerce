from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from EcommApp.models.user import User

class UserProfile(View):
    def get(self, request):
        return render(request, 'userprofile.html')
    
    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        profileImg = request.FILES.get("profileImg")

        user = User.get_customer_by_email(email)
        
        if user:
            # Update user details
            user.fname = fname
            user.lname = lname
            user.phone = phone
            user.email = email
            
            if profileImg:
                user.profileImg = profileImg

            user.save()

            # Update session data
            request.session['user_fname'] = fname
            request.session['user_lname'] = lname
            request.session['user_phone'] = phone
            request.session['user_email'] = email
            if profileImg:
                request.session['user_profileImg'] = user.profileImg.url

            # Success message
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('home')  # Replace 'home' with the appropriate redirect URL
        else:
            # Error message
            messages.error(request, "User not found. Please try again.")
            return redirect('userprofile')

