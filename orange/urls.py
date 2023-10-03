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
from django.conf import settings
from django.conf.urls.static import static
from user_payment.views import payment_cancelled, payment_successful, product_page, stripe_webhook
from .view import login_view, main_view , register_view
from django.contrib.auth.views import LogoutView
from Profiles.views import my_profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main_view'),
    path('register/', register_view, name='register_view'),
    path('login/', login_view, name='login_view'),
    path('profile/', my_profile_view, name='my_profile_view'),
    path('product_page/', product_page, name='product_page'),
    path('payment_successful/', payment_successful, name='payment_successful'),
    path('payment_cancelled/', payment_cancelled, name='payment_cancelled'),
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<str:code>/', main_view, name='main'),
# Match the root URL with no 'code' parameter
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)