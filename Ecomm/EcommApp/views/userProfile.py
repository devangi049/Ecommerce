from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from EcommApp.models.user import User

class UserProfile(View):
    def get(self, request):
        return render(request, 'userprofile.html')
    
    def post(self, request):
        postData = request.POST
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        profileImg = request.FILES.get("profileImg")

        value = {
            "fname": fname,
            "lname": lname,
            "phone": phone,
            "email": email,
            "profileImg": profileImg
        }
        
        print(value)

        user = User.get_customer_by_email(email)
        error_message = None
        
        if user:
            print("User:", user)
            request.session['user'] = user.id
            
            print(request.FILES)

            if profileImg:
                user.profileImg = profileImg

            user.fname = fname
            user.lname = lname
            user.phone = phone
            user.email = email
            
            user.save()
          
            request.session['user_fname'] = fname
            request.session['user_lname'] = lname
            request.session['user_phone'] = phone
            request.session['user_email'] = email
            if profileImg:
                request.session['user_profileImg'] = user.profileImg.url
            
            # Use the messages framework for feedback
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('home')  # Ensure 'home' is a valid named URL in your URLs configuration
        
        return render(request, 'userprofile.html', {'error': error_message})
