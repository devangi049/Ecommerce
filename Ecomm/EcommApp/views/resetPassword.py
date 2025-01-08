from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views import View
from EcommApp.models.user import User
from django.contrib.auth.hashers import make_password

class ResetPassword(View):
    def get(self,request):
        return render(request,'resetpassword.html')
    
    def post(self,request):
        new_password = request.POST.get('newPassword')
        confirmNew_password = request.POST.get('confirmNewPassword')

        if new_password == confirmNew_password:
            email = request.session.get('email')
            user = User.objects.filter(email=email).first()

            if user:
                hashed_password = make_password(new_password)
                user.password = hashed_password
                user.save()

                return redirect('login')
            else:
                error_message="User not found"
                return render(request,"resetpassword.html",{"error":error_message})
            
        else:
            error_message="Passwords do not match. Please try again."
            return render(request,"resetpassword.html",{"error":error_message})