
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.
from .forms import CreateUserForm
from .decorators.decorators import admin_permissions, autheticated_user, unautheticated_user, autheticated_user

@autheticated_user
@admin_permissions
def register(response):
    form = CreateUserForm()
    if response.method == 'POST':
        form = CreateUserForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect(homePage)
    context = {'form':form}
    return render(response, "accounts/register.html", context)

@unautheticated_user
def loginPage(request):
    messages.info(request, 'Session logged correctly')
    context = {}
    if request.method=='POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(homePage)
        else:
           return render(request, 'accounts/login.html', context)
    return render(request, 'accounts/login.html', context)

@autheticated_user
def homePage(request):
    context = {"user":request.user}
    return render(request, 'accounts/home.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

