"""orange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .view import main_view , register_view
from django.contrib.auth.views import LogoutView
from Profiles.views import my_profile_view
from user_payment.views import product_page, payment_successful, payment_cancelled, stripe_webhook
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main_view'),
    path('register/', register_view, name='register_view'),
    path('profile/', my_profile_view, name='my_profile_view'),
    path('product_page/', product_page, name='product_page'),
    path('payment_successful/', payment_successful, name='payment_successful'),
    path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<str:code>/', main_view, name='main'),

]
