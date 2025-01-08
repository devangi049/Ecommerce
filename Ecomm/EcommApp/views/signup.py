from django.views import View
from django.shortcuts import render,redirect
from EcommApp.models.user import User
from django.contrib.auth.hashers import make_password

class Signup(View):

    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        postData= request.POST
        fname= postData.get("fname")
        lname= postData.get("lname")
        phone= postData.get("phone")
        email= postData.get("email")
        password = postData.get("password")
        confirmPassword = postData.get("confirmPassword")
        profileImg= request.FILES.get("profileImg")

        value = {
            "fname":fname,
            "lname":lname,
            "phone":phone,
            "email":email
        }

        error_message= None
        
        user=User(
            fname=fname,
            lname=lname,
            phone=phone,
            email=email,
            password=password,
             profileImg=profileImg
        )

        error_message=self.validateUser(user,confirmPassword)
        
        if not error_message:
            user.password = make_password(user.password)
            user.save()

            return redirect('/login')
        else:
            #return the form with error message
            data = {
                'error':error_message,
                "values": value
            }
            return render(request, 'signup.html',data)
        
    def validateUser(self, user, confirmPassword):
        error_message =None
        if not user.fname:
            error_message = "First Name Required!"
        elif len(user.fname)<4:
            error_message = "First name must be 4 characters long or more."
        elif not user.lname:
            error_message = "Last Name Required!"
        elif len(user.lname)<4:
            error_message="Last name must be 4 characters long or more."
        elif not user.phone:
            error_message = "Phone Number Required!"
        elif len(user.phone)<10:
            error_message = "Phone number must be 10 characters long."
        elif not user.password:
            error_message = "Password is required!"
        elif len(user.password)<6:
            error_message = "Password must be 6 characters long."
        elif user.password != confirmPassword:
            error_message = "Password and confirm password do not match."
        elif len(user.email)<6:
            error_message = "Email must be 6 characters long."
        elif user.isExists():
            error_message = "Email already exists."
            
        return error_message