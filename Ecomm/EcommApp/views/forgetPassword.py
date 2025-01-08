from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views import View
from EcommApp.models.user import User
import random
from django.core.mail import send_mail

otp_storage={}

class ForgetPassword(View):
    
    def get(self, request):
        return render(request,'forgetpassword.html')
    
    def post(self,request):
        email=request.POST.get('email')
        
        user=User.objects.filter(email=email).first()


        if user:
            otp = random.randint(100000, 999999)
            otp_storage[email] = otp
            print(f"OTP stored for {email}: {otp}")  # Debugging line
            
            # Store email in session
            request.session['otp'] = otp
            request.session['email'] = email
            request.session.save() 
            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is: {otp}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            print(otp_storage)
            
            
            return redirect('/verify-otp')

        else:
            error_message = "Email does not exist."
            return render(request, 'forgetpassword.html', {'error': error_message})

