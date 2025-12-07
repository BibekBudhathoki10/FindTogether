from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser
from .forms import RegistrationForm, LoginForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create_user(
                phone_number=form.cleaned_data['phone_number'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                address=form.cleaned_data['address'],
                role='normal'
            )
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            
            print(f"[v0] Login attempt - Phone: {phone_number}")
            
            try:
                check_user = CustomUser.objects.get(phone_number=phone_number)
                print(f"[v0] User found in database: {check_user}")
                print(f"[v0] Stored password hash: {check_user.password}")
            except CustomUser.DoesNotExist:
                print(f"[v0] User does not exist with phone: {phone_number}")
            
            # Authenticate using phone number
            user = authenticate(request, username=phone_number, password=password)
            
            print(f"[v0] Authentication result: {user}")
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid phone number or password.')
        else:
            print(f"[v0] Form errors: {form.errors}")
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'dashboard.html', {'user': request.user})
