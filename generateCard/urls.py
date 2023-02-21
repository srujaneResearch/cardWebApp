from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('signup',views.singup,name='signup'),
    path('loginAuth',views.loginAuth,name='loginAuth'),
    path('register',views.register,name='register'),
    path('logout',views.logoutAuth,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('checkCardBalance/<int:card_no>',views.getCardBalance,name='cardbalance'),
    path('checkoutCoinpayment',views.checkoutCoinpayments,name='checkout'),
    path('topup/<int:card_no>',views.topupCard,name='topup'),
    path('transactionlog/<int:card_no>',views.getTransactionLog,name='transaction'),
    path("getCardFee/<int:card_type>",views.getCardTypeInfo,name='cardfee'),
    path('coinpaymentWebhook',views.coinpaymentWebhook,name='coinpaymentWebhook'),
    path('cron1',views.exeUpdateUser,name='c1'),
    path('forgotpassword',views.forgot,name='forgot'),
    path('changecred',views.changeUser,name='cuser'),
    path('account-recovery/<str:sessiond>',views.passChangeView,name='accrecover'),
    path('account-2FA-secure/<str:sessiond>',views.OTPView,name='2fa'),
    path('account-secure-2FA-complete/<str:sessiond>',views.check2FA,name='2faauth'),
    path('account-reset-done/<str:sessiond>',views.accResetView,name='resetconfirm'),
    ]