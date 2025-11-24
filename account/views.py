from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    """ورود کاربران"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if hasattr(user, 'shop'):
                return redirect('shop_dashboard')
            if user.is_superuser:
                return redirect('/admin/')
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def shop_dashboard(request):
    return render(request, 'account/shop_dashboard.html')

@login_required
def profile_view(request):
    return render(request, "profile/profile.html")
