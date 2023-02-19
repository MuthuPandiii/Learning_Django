from django.shortcuts import render
from App1.forms import User_Form,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'App1/index.html')

def register(request):
    registered  = False

    if request.method == "POST":
        user_form = User_Form(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'protfolio_pic' in request.FILES:
                profile.portfolio_pic = request.FILES['portfolio_pic']
            profile.save()
            registered = True
        
        else:
            print(user_form.errors,profile_form.errors)
    
    else:
        user_form = User_Form()
        profile_form = UserProfileInfoForm()


    return render(request,'App1/register.html',context={'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('The Account is no longer Active')
        else:
            return HttpResponse('No Account Found')
    return render(request,'App1/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))