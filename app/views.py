from django.shortcuts import render
from app.fomrs import *
from django.http import HttpResponse
from django.core.mail import send_mail

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
           'Hi bro had you completed your dinner',
           'ramperupogu@gmail.com',
           [UI.email],
           fail_silently=False)

           return HttpResponse('Registration is Success')

    return render(request,'registration.html',d)