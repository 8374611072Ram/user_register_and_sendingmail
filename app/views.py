from django.shortcuts import render
from app.fomrs import *
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app.models import *

# Create your views here.
def home(request):
    return render(request,'home.html')

def registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}

    if request.method=='POST' and request.FILES:
        ud=UserForm(request.POST)
        pd=ProfileForm(request.POST,request.FILES)
        if ud.is_valid() and pd.is_valid():
            UI=ud.save(commit=False)
            pw=ud.cleaned_data.get('password')
            UI.set_password(pw)
            UI.save()
            PI=pd.save(commit=False)
            PI.user=UI
            PI.save()
            send_mail('registration',
                'I Love you Baby Thinva And nuvu nakosam epudu vastavu',
                'ramperupogu@gmail.com',
                [UI.email],
                fail_silently=False)
            return HttpResponse('Registration is Success')         
    return render(request,'registration.html',d)


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request, user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid User')

    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(user=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        username=request.session.get('username')
        uo=User.objects.get(username=username)
        pw=request.POST['password']
        uo.set_password(pw)
        uo.save()
        return HttpResponse('Password is changed Successfully')
    return render(request,'change_password.html')

def reset_password(request):
    if request.method=='POST':
        un1=request.POST['username']
        pw1=request.POST['password']
        UO1=User.objects.get(username=un1)
        UO1.set_password(pw1)
        UO1.save()
        return HttpResponse('Reset password is suucessful')
    return render(request,'reset_password.html')