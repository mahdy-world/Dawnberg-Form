from django.shortcuts import redirect, render
from django.views.generic import *
from django.contrib.auth import authenticate, login

# Create your views here.

class Login(View):
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('Core:index')
            else:
                error = 'تم ايقاف الحساب الخاص بك '
                return render(request, 'Auth/login.html' , context={'error':error}) 
        else:
                error = 'برجاء التأكد من اسم المستخدم وكلمة المرور'
                return render(request, 'Auth/login.html' , context={'error':error})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('Core:index')
        return render(request,'Auth/login.html')                   
