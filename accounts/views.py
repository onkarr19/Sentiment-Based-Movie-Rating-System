from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is None:
            user = auth.authenticate(email=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')

        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            username = request.POST.get('username')
            email = request.POST.get('email')
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password1)
                user.save()
                auth.login(request, user)
                messages.info(request, 'Account Created')
                return redirect('/')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')
    else:
        return render(request, 'register.html')


def user_logout(request):
    auth.logout(request)
    return redirect('/')


def user_details(request):
    if request.user.is_authenticated:
        return redirect('/')
        # return render(request, 'userprofile.html')
    else:
        messages.error(request, 'You Need to Login First!')
        return redirect('/')
