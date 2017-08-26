from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserLoginForm

def login_view(request):
    '''Login form for user authentication'''
    # If the user is already logged in, redirect to the todo page
    if request.user.is_authenticated:
       return redirect('/todo/')
    
    # If the user attempts to go to another url without logging in, remember
    # the that url in next
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    # If the form is valid, attempt to authenticate and login the user
    if form.is_valid():
        username = form.cleaned_data.get("user")
        password = form.cleaned_data.get("password")
        
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            # Redirect to original url after logging in
            return redirect(next)
        # After logged in, go to todo page
        return redirect('/todo/')

    # If user is not logged in, show the login page. 
    return render(request, "login/login.html", {"form":form})

def logout_view(request):
    '''Logout the user - go to /login/logout'''
    logout(request)
    # Redirect to login page after logging user out
    return redirect('/login/')