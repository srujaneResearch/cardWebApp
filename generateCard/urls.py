from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('singup',views.singup,name='singup'),
    path('loginAuth',views.loginAuth,name='loginAuth'),
    path('register',views.register,name='register'),
    path('logout',views.logoutAuth,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('checkoutCoinpayment',views.checkoutCoinpayments,name='checkout'),
    #path('generateCardUSD',views.generateCardUSD,name="generateUSD"),
    path('coinpaymentWebhook',views.coinpaymentWebhook,name='coinpaymentWebhook')
    ]