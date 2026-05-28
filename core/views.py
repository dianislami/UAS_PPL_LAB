import json
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from coins.models import Coin
from core.utils import seed_all

def landing_page(request):
    seed_all()
    # Ambil 3 koin teratas untuk slider/baris fitur
    featured = Coin.objects.all().order_by('rank')[:3]
    return render(request, 'core/landing.html', {'featured_coins': featured})

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
        
    error_msg = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Otomatis create "admin/admin123" superuser jika tidak ada
        if username == 'admin' and password == 'admin123':
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
                
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error_msg = "Username atau password yang dimasukkan salah. Silakan coba kembali."
            
    return render(request, 'core/login.html', {'error': error_msg})

def admin_logout(request):
    logout(request)
    return redirect('landing_page')
