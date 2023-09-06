from django.shortcuts import render
from app.forms import *
# Create your views here.
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


def Home(request):
    
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        
        return render(request,'Home.html',d)
        
    return render(request,'Home.html')


def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()
            
            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()
            
            send_mail('Registration',
                      'Done successfully!!',
                      'cchandu6136@gmail.com',
                      [NSUO.email],
                      fail_silently=False
                      )
            
            return HttpResponse('Registration is successfully Done !!!')
        else:
            return HttpResponse(' Not Valid ')
    
    
    return render(request,'registration.html',d)


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request, AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('Home'))
        else:
            return HttpResponse('Invalid username or Password')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Home'))

@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)    
@login_required
def change_password(request):
    if request.method=='POST':
        PW=request.POST['PW']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(PW)
        UO.save()
        return HttpResponse("<center><h1  style='color:blue;'>password changed successfully!!!</h1></center>")
    return render(request, 'change_password.html')

def reset(request):
    if request.method=='POST':
        password=request.POST['password']
        username=request.POST['username']
        LUO=User.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('password is reseted successfully!!')
        else:
            return HttpResponse("<center><h1  style='color:blue;'>user is not there in DataBase!!!</h1></center>")
    return render(request,'reset.html')