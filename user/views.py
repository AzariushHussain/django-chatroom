from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.db import IntegrityError
from django.core.exceptions import ValidationError

def register(request):
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your account has been created successfully. You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'There was an error with your registration form. Please check the fields and try again.')
        else:
            form = UserCreationForm()
        return render(request, 'user/register.html', {'form': form})
    
    except IntegrityError as e:
        messages.error(request, 'There was a database error while creating your account. Please try again later.')
        print(f"IntegrityError: {e}")
        return render(request, 'user/register.html', {'form': form})
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please try again later.')
        print(f"Exception in register: {e}")
        return render(request, 'user/register.html', {'form': form})

def login(request):
    try:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()  
                auth_login(request, user)  
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('room')  
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            form = AuthenticationForm()  
        return render(request, 'user/login.html', {'form': form})
    
    except ValidationError as e:
        messages.error(request, f'Invalid input: {e.message}')
        print(f"ValidationError: {e}")
        return render(request, 'user/login.html', {'form': form})
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please try again later.')
        print(f"Exception in login: {e}")
        return render(request, 'user/login.html', {'form': form})

def logout(request):
    try:
        print("inside logout")
        auth_logout(request)
        return redirect('login')
    
    except Exception as e:
        messages.error(request, 'An error occurred while logging out. Please try again later.')
        print(f"Exception in logout: {e}")
        return redirect('room')
