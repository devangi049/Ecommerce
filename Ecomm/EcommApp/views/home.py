from django.shortcuts import redirect,render
from django.views import View

class Index(View):

    def get(self,request):
        return render(request,"index.html")
    
    