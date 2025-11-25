from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
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
    user = request.user
    profile, _ = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save(user=user)
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

    return render(request, 'profile/profile.html', {'form': form})


