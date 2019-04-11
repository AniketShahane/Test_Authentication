from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.core.mail import send_mail

def home(request):
    if request.user.is_authenticated:
        return redirect('success')
    return render(request, 'home.html')

def login(request):
    correct_credentials = {'valid': True}
    if request.method == 'POST':
        if request.POST['email'] != '' and request.POST['password'] != '':
            email = request.POST['email']
            password = request.POST['password']
            username = User.objects.filter(email=email)
            if username:
                user = authenticate(request, username=username[0], password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('success')
                else:
                    correct_credentials['valid'] = False
                    correct_credentials['message'] = 'Incorrect credentials'
                    return render(request, 'login.html', {'correct_credentials': correct_credentials})
            else:
                correct_credentials['valid'] = False
                correct_credentials['message'] = 'Incorrect credentials'
                return render(request, 'login.html', {'correct_credentials': correct_credentials})
    else:
        if request.user.is_authenticated:
            return redirect('success')
        return render(request, 'login.html', correct_credentials)

def success(request):
    return render(request, 'success.html', {'name': request.user.first_name})

def logout(request):
    auth.logout(request)
    return redirect('home')

def register(request):
    email_validate = {'valid': True}
    password_match = {'valid': True}
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            password_match['valid'] = False
            password_match['message'] = 'Passwords dont match !!'
            return render(request, 'register.html', {'email_validate': email_validate, 'password_match': password_match})
        elif len(password) < 8:
            password_match['valid'] = False
            password_match['message'] = 'Password should at least be 8 characters long !!'
            return render(request, 'register.html', {'email_validate': email_validate, 'password_match': password_match})
        else:
            password_match['valid'] = True
            if User.objects.filter(email=email):
                email_validate['valid'] = False
                email_validate['message'] = 'Email already exists!!'
                return render(request, 'register.html', {'email_validate': email_validate, 'password_match': password_match})
            else:
                new_user = User.objects.create_user(email=email, username=email, password=password, first_name=name.split()[0])
                new_user.save()
                send_mail(subject='Successful Registration', message=f'Hi {name.split()[0]}, you have been successfully registered with the username {email}', from_email='test.authentication.321@gmail.com', recipient_list=(email, 'theflash.299792458@gmail.com'))
                return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('success')
        return render(request, 'register.html', {'email_validate': email_validate, 'password_match': password_match})