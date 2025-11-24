from django.urls import path
from .views import login_view, logout_view, shop_dashboard, profile_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('shop_dashboard/', shop_dashboard, name='shop_dashboard'),
    path('profile/', profile_view, name='profile'),
]
