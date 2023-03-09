
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.http.response import HttpResponseBadRequest
from django.utils.http import urlencode
# Create your views here.
from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import mysql.connector
from django.contrib.auth.models import User
from generateCard import card
from generateCard.models import CardGenerated,CardTypes,TopupCard,UserWallet,InitialPayment,AuthTokens,TwoFAAuth
from generateCard import forms
from django.views.decorators.csrf import csrf_exempt
from generateCard import pyCoinpayments
from datetime import datetime,timedelta
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

from cardWebApp.settings import ALLOWED_HOSTS
from django.urls import reverse
coin_pub = "d9c1815b8809bc4627561eda3a185528645f7bbe57ed97f94b3e8e1a78a03ca5"
coin_pvt = "F3Daf74154b0597Cf8cB69eEb0A782f85D0cdfE7a4644dAAdeD655987Ec27866"
import pytz
def accessUser(email):
    db = mysql.connector.connect(host="server07.hostfactory.ch",user="card_wepapp",password="E9ytaGuMAtAMuBUh",database="Token")

    cur = db.cursor()
    cur.execute("select * from users where email='{0}'".format(email))
    l = cur.fetchall()

    return l

@csrf_exempt
def coinpaymentWebhook(request):
    if request.method == 'POST':
        import hmac
        import hashlib
        print("this is requet", request)
        #print(request.POST)
        #print(request.body,'\n')
        #print(request)
        #print(request.META)
        print(request.headers)
        print(request.headers['Hmac'])
        encoded_ = request.body
        hashcode = hmac.new(bytearray('Soul1234', 'utf-8'), encoded_, hashlib.sha512).hexdigest()
        print("our hmac body",hashcode)


        if 'Hmac' in request.headers.keys():
            if hashcode == request.headers['Hmac']:
                txn_id = request.POST['txn_id']
                tx_status = int(request.POST['status'])
                try:
                    print(request.POST)
                    if request.POST['custom']=='top up':
                        ipay = TopupCard.objects.get(coinpayment_tx_hash=txn_id)
                    else:
                        ipay = InitialPayment.objects.get(coinpayment_tx_hash=txn_id)
                except:
                    print("no tx found",txn_id)
                    return HttpResponseBadRequest("tx not found", txn_id)
                
                if ipay.payment_status == 'rejected' or ipay.payment_status == 'successful':
                    return HttpResponse(status=200)
                
                else:
                    #check payment status
                    if tx_status == 100:

                        if request.POST['custom']=='top up':
                            print(request.POST)
                            c_no = ipay.card.card_number
                            amt = int(ipay.amount)
                            c_instance = CardGenerated.objects.get(card_number=c_no)
                            res = card.topUpCard(amt,c_no)
                            print(res)
                            if res['success']:
                                c_instance.card_balance = c_instance.card_balance+ipay.amount
                                c_instance.save()
                                ipay.payment_status = 'successful'
                                ipay.timestamp_finished = datetime.now()
                                ipay.save()
                                return HttpResponse(status=200)
                            else:
                                print("API Fails For Top Up")
                                return HttpResponseBadRequest("API FAIL FOR TOPUP")
                        else:

                            name,surname = ipay.card_holder_name,ipay.card_holder_surname
                            amount,addl1 = ipay.amount,ipay.card_holder_addressline1
                            addl2,city = ipay.card_holder_addressline2,ipay.card_holder_city
                            state,country = ipay.card_holder_state,ipay.card_holder_country
                            zipcode,cardtype = ipay.card_holder_zip,ipay.card_type.card_type
                            res = card.issueCard(name,surname,amount,addl1,addl2,city,state,country,zipcode,cardtype)
                            print(res)
                            if res['success']:
                                card_number,card_exm,card_exy,card_cvv,balance = int(res['message']['card_info']['card_number']),int(res['message']['card_info']['card_exp_mth']),int(res['message']['card_info']['card_exp_year']),int(res['message']['card_info']['card_cvv']),res['message']['card_balance']['balance']

                                ct = CardTypes.objects.filter(card_type=cardtype)[0]
                                c = CardGenerated()
                                c.card_type = ct
                                c.card_holder_user = ipay.user
                                c.card_number = card_number
                                c.identify_walletaddress = ipay.identify_walletaddress
                                c.card_holder_name = name
                                c.card_holder_surname = surname
                                c.card_expiry_month = card_exm
                                c.card_expiry_year = card_exy
                                c.card_cvv = card_cvv
                                c.card_holder_addressline1 = addl1
                                c.card_holder_addressline2 = addl2
                                c.card_holder_city = city
                                c.card_holder_country = country
                                c.card_holder_zip = zipcode
                                c.initial_payment_id = ipay
                                c.card_balance = balance
                                c.save()
                                ipay.payment_status = 'successful'
                                ipay.timestamp_finished = datetime.now()
                                ipay.save()
                                return HttpResponse(status=200)
                            else:
                                print("API Fails For Card generation")

                                return HttpResponseBadRequest("API FAILS TOPUP")
                    
                    elif tx_status < 0:
                        ipay.payment_status = "rejected"
                        ipay.timestamp_finished = datetime.now()
                        ipay.save()
                        return HttpResponse(status=200)
                    elif tx_status == 1:
                        ipay.payment_status = "approved"
                        ipay.save()
                        return HttpResponse(status=200)
                    else:
                        ipay.payment_status = "pending"
                        ipay.save()
                        return HttpResponse(status=200)
            else:
                return HttpResponseBadRequest('BAD Request HMAC')
        else:
            return HttpResponseBadRequest('BAD Request HMAC')
    else:
        return HttpResponse(status=200)

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')    
    return render(request, 'generateCard/login.html',context={'active':True,'status':True,'ico':True,'block':False})

def singup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
    return render(request,'generateCard/signup.html',context={'status':True,'user':False})


def forgot(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
    return render(request,'generateCard/forgotpass.html',context={'status':True,'req':False})

#session protected view
def passChangeView(request,sessiond):
    try:
        uget = AuthTokens.objects.get(token=sessiond)
        return render(request,'generateCard/recoverpass.html',context={'sess':sessiond,'status':False,'expiry':False})
    except:
        print("No user")
        return HttpResponseBadRequest("Invalid request!")
#session protected view
def accResetView(request,sessiond):
    if request.method == 'POST':
        password = request.POST['password']
        try:
            uget = AuthTokens.objects.get(token=sessiond)
            usr = User.objects.get(username=uget.user.username)
            utc = pytz.UTC
            if uget.status == True and utc.localize(datetime.now()) < uget.expiry:
                usr.set_password(password)
                usr.save()
                uget.status=False
                uget.save()
                print("Password reset successful.")
                return render(request,'generateCard/recoverpass.html',context={'sess':sessiond,'status':True,"expiry":False})
            else:
                uget.status=False
                uget.save()
                print("session expired")
                return render(request,'generateCard/recoverpass.html',context={'sess':sessiond,'status':False,"expiry":True})
        except:
            print("user not exsist")
            return HttpResponseBadRequest("Invalid Request")
    else:
        return HttpResponseBadRequest("Invalid request!")
    
    

def createPasswordToken(usr):
    try:
        uget = AuthTokens.objects.get(user=usr)
        import uuid
        tkn = str(uuid.uuid4())
        uget = AuthTokens.objects.get(user=usr)
        uget.status = True
        uget.token = tkn
        uget.date_requested = datetime.now()
        uget.expiry = datetime.now()+timedelta(minutes=30)
        uget.save()
        subject="PASSWORD RESET REQUEST | ETERNALCARD"
        msg="click on below link to change your password. Link is valid only for 30 minutes.\n\n{0}".format("https://"+ALLOWED_HOSTS[0]+"/account-recovery/"+tkn)
        send_mail(subject=subject,message=msg,from_email="card@neweternallife.net",recipient_list=[usr.email])
        #return tkn       
    except:
        import uuid
        tkn = str(uuid.uuid4())
        uget = AuthTokens()
        uget.user = usr
        uget.status = True
        uget.token = tkn
        uget.date_requested = datetime.now()
        uget.expiry = datetime.now()+timedelta(minutes=30)
        uget.save()
        subject="PASSWORD RESET REQUEST | ETERNALCARD"
        msg="click on below link to change your password. Link is valid only for 30 minutes.\n\n{0}".format("https://"+ALLOWED_HOSTS[0]+"/account-recovery/"+tkn)
        send_mail(subject=subject,message=msg,from_email="card@neweternallife.net",recipient_list=[usr.email])
        #return tkn


def changeUser(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))

    if request.method == 'POST':
        email= request.POST['email']
        try:
            k = User.objects.get(username=email)
            if k.is_active:
                print("active")
                createPasswordToken(k)
                return render(request,'generateCard/forgotpass.html',context={"status":True,"req":True})
            else:
                return render(request,'generateCard/forgotpass.html',context={"status":False,"req":False})
        except:
            print("user not exsist")
            return render(request,'generateCard/signup.html',context={"status":False,"user":False})
    else:
        return HttpResponseRedirect('/')

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))    
    if request.method == 'POST':
        email,password = request.POST['email'],request.POST['password']
        try:
            k = User.objects.get(username=email)
            if k.is_active:
                return render(request,'generateCard/signup.html',context={"status":True,"user":True})
        except:
            print("user not exsist")
            return render(request,'generateCard/signup.html',context={"status":False,"user":False})
        
        print(request.method)

        k.is_active = True
        k.set_password(password)
        k.save()
        login(request,k)
        return HttpResponseRedirect('/dashboard')         
    else:
        return HttpResponseBadRequest("Invalid request")


def create2FACode(usr):
    try:
        import uuid
        tkn = str(uuid.uuid4())
        uget = TwoFAAuth.objects.get(user=usr)
        uget.status = True
        uget.token = tkn
        uget.date_requested = datetime.now()
        uget.expiry = datetime.now()+timedelta(minutes=30)
        import random
        otp = random.randint(100000,999999)
        uget.otp = otp
        uget.attempt=1
        uget.save()
        subject="OTP FOR LOGIN | ETERNALCARD"
        msg="One time password for login is.\n\n{0}".format(otp)
        send_mail(subject=subject,message=msg,from_email="card@neweternallife.net",recipient_list=[usr.email])
        return tkn       
    except:
        import uuid
        tkn = str(uuid.uuid4())
        uget = TwoFAAuth()
        uget.user = usr
        uget.status = True
        uget.token = tkn
        uget.date_requested = datetime.now()
        uget.expiry = datetime.now()+timedelta(minutes=30)
        import random
        otp = random.randint(100000,999999)
        uget.otp = otp
        uget.attempt=1
        uget.save()
        subject="OTP FOR LOGIN | ETERNALCARD"
        msg="One time password for login is.\n\n{0}".format(otp)
        send_mail(subject=subject,message=msg,from_email="card@neweternallife.net",recipient_list=[usr.email])
        return tkn

def sendBlockEmail(eml):
    subject="[ Action Required ] | ETERNALCARD"
    msg="Your account is blocked for 15 minutes after 3 unsuccessful password attempts!"
    send_mail(subject=subject,message=msg,from_email="card@neweternallife.net",recipient_list=[eml])    


def check2FaBlock(usr):
    try:
        uget = TwoFAAuth.objects.get(user=usr)
        if uget.block:
            utc=pytz.UTC
            if utc.localize(datetime.now())>uget.block_time_over:
                uget.block = False
                uget.save()
                return False
            else:
                return True
        else:
            return False
    except:
        print("2fa block check error")
        return False


def loginAuth(request):
    print(request.POST,'\n\n',request)
    if request.method=='POST':
        print("login view")
        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard')
        else:
            if 'remember' not in request.POST.keys():
                request.session.set_expiry(0)

            username,password = request.POST['email'],request.POST['password']
            try:
                uget = User.objects.get(username=username)
                if not uget.is_active:
                    return render(request,'generateCard/login.html',context={'active':False,'status':True,'ico':True,'block':False})
                else:
                    user = authenticate(username=username,password=password)
                    print(user)
                    if user is not None and (not check2FaBlock(uget)):
                        print("2FA")
                        #login(request,user)
                        tkn = create2FACode(uget)
                        return HttpResponseRedirect(reverse('2fa',args=(tkn,)))
                    else:
                        print("not")
                        status = True
                        ico=True
                        active=True
                        return render(request,'generateCard/login.html',context={'active':active,'status':status,'ico':ico,'block':True})

            except ObjectDoesNotExist:
                print("error")
                return render(request,'generateCard/signup.html',context={'status':False,'user':False})
    else:
        return HttpResponseBadRequest("Invalid Request")

def OTPView(request,sessiond):
    if request.user.is_authenticated:
        print("Dashboard")
        return HttpResponseRedirect('/dashboard')
    else:
        print("onetime")
        return render(request,'generateCard/onetime.html',context={"status":True,"attempt":3,'sess':sessiond})

def check2FA(request,sessiond):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
    if request.method == 'POST':
        password = request.POST['password']
        print(password)
        try:
            uget = TwoFAAuth.objects.get(token=sessiond)
            usr = User.objects.get(username=uget.user.username)
            utc = pytz.UTC
            #-----------session expiry-------------
            if uget.status == False:
                return HttpResponseBadRequest("Session Expired!")
            
            #-----------status True and time left and otp right-------------
            elif uget.status == True and utc.localize(datetime.now()) < uget.expiry and uget.otp==int(password):
                login(request,usr)
                uget.status=False
                uget.save()
                print("login complete")
                return HttpResponseRedirect(reverse('dashboard'))
            #-----------status true, time exceeds and otp true-------------

            #-----------status true and time left, otp wrong-------------
            elif uget.status == True and utc.localize(datetime.now()) < uget.expiry and uget.otp!=int(password) and uget.attempt<=3:
                
                if uget.attempt == 3:
                    uget.attempt=uget.attempt+1
                    aleft = 3-uget.attempt
                    uget.status=False
                    uget.block = True
                    uget.block_time_over = datetime.now()+timedelta(minutes=15)
                    uget.save()                    
                    return render(request,'generateCard/onetime.html',context={'sess':sessiond,'status':False,"attempt":-1})
                                    
                uget.attempt=uget.attempt+1
                aleft = 3-uget.attempt
                uget.save()
                return render(request,'generateCard/onetime.html',context={'sess':sessiond,'status':False,"attempt":aleft})          
            else:
                uget.status=False
                uget.save()
                print("session expired")
                return HttpResponseBadRequest("Session Expired!")
        except:
            print("user not exsist")
            return HttpResponseRedirect('/')
    else:
        return HttpResponseBadRequest("Invalid Request")

def logoutAuth(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/')
def dashboard(request):

    user = request.user
    print(request.user.username)
    try:
        udb = accessUser(user.username)[0]
        print(udb)
        token_balance,wallet = udb[16],udb[13]
        if token_balance == None:
            token_balance = 0
        if wallet == None:
            wallet = "NA"
        emailaddr = udb[2]
    except:
        token_balance,wallet,emailaddr = 0,"NA",request.user.email

    c = CardTypes.objects.all()
    cards_generated = CardGenerated.objects.filter(card_holder_user=request.user)
    if len(cards_generated)==0:
        card_status = False
    else:
        card_status=True
    cform = forms.GenerateCardForm()
    tform = forms.TopupForm()
    print(card_status)
    print(cards_generated)
    #card_status=False
    if card_status:
        balance = 0
        for _ in cards_generated:
            balance+=_.card_balance
    else:
        balance = 0
    context = {'tokenBalance':token_balance,
                'wallet':wallet,
                'emailaddress':emailaddr,
                'cardTypes':c,
                'card_status':card_status,
                "cardgenerated":cards_generated,
                "cform":cform,
                "cbalance":balance,
                "tform":tform,
    }
    return render(request,'generateCard/dashboard.html',context)


@login_required(login_url='/')
def checkoutCoinpayments(request):
    udb = accessUser(request.user.email)[0]
    token_bal,wallet = int(udb[16]),udb[13]
    if token_bal < 2499:
        HttpResponseRedirect('/dashboard')
    else:
        if request.method=='POST':
            print(request.POST)
            name,surname,amount,addl1,addl2,city,state,country,zipcode,cardtype = request.POST['name'],request.POST['surname'],request.POST['amount'],request.POST['addl1'],'---',request.POST['city'],request.POST['state'],request.POST['country'],request.POST['zipcode'],request.POST['cardtype']
            coin = request.POST['crypto']
            print(name)
            amount = int(amount)

            paycoin = pyCoinpayments.CryptoPayments(coin_pub,coin_pvt,'http://eternalcard.net/coinpaymentWebhook')
            cdetails = CardTypes.objects.get(card_type=int(cardtype))
            
            c_fee = cdetails.card_generatefee + cdetails.card_topup_fixfee + ((cdetails.card_topup_percentfee/100)*amount)
            total_amt = amount+c_fee
            pamt = (0.0075*total_amt)+total_amt
            
            tx_para = {
                'amount':pamt,
                'currency1':'USD',
                'currency2':coin,
                'buyer_email':request.user.email,
                'buyer_name':wallet,
                'custom':'initial payment'
            }

            txn = paycoin.createTransaction(tx_para)
            ipayrecord = InitialPayment()
            ipayrecord.user = request.user
            ipayrecord.identify_walletaddress = wallet
            ipayrecord.amount = int(amount)
            ipayrecord.payment_amount = pamt #amount+((0.75/100)*amount)
            ipayrecord.payment_type = 'coinpayment'
            ipayrecord.coinpayment_tx_hash = txn['txn_id']
            ipayrecord.payment_status = 'initiated'
            ipayrecord.card_type = CardTypes.objects.filter(card_type=cardtype)[0]
            ipayrecord.card_holder_name = name
            ipayrecord.card_holder_surname = surname
            ipayrecord.card_holder_addressline1 = addl1
            ipayrecord.card_holder_addressline2 = addl2
            ipayrecord.card_holder_city = city
            ipayrecord.card_holder_state = state
            ipayrecord.card_holder_country = country
            ipayrecord.card_holder_zip = zipcode
            ipayrecord.save()

            return HttpResponseRedirect(txn['checkout_url'])
        else:
            return HttpResponseRedirect('/dashboard')

@login_required(login_url='/')
def getCardBalance(request,card_no):
    if request.user.is_authenticated:
        gt_card = CardGenerated.objects.get(card_holder_user=request.user,card_number=card_no)
        res = card.getBalance(card_no)
        print(res)
        if res['success']:
            balance = res['data']['balance']
            gt_card.card_balance = balance
            gt_card.save()
            return HttpResponseRedirect('/dashboard')
        else:
            print("Balance API Error")
            return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/')
def topupCard(request,card_no):
    if request.user.is_authenticated:
        wallet = UserWallet.objects.get(user=request.user)
        gt_card = CardGenerated.objects.get(card_holder_user=request.user,card_number=card_no)
        if request.method=='POST':
            print(request.POST)
            amount = request.POST['Amount']
            amount = int(amount)

            if gt_card.card_balance+amount > gt_card.card_type.card_balance_limit:
                return HttpResponseRedirect('/dashboard')
            coin = request.POST['crypto']
            paycoin = pyCoinpayments.CryptoPayments(coin_pub,coin_pvt,'http://eternalcard.net/coinpaymentWebhook')            
            tfees = gt_card.card_type.card_topup_fixfee + (gt_card.card_type.card_topup_percentfee/100)*amount
            tamount = amount+tfees
            pamt = 0.0075*tamount + tamount
            tx_para = {
                'amount':pamt,
                'currency1':'USD',
                'currency2':coin,
                'buyer_email':request.user.email,
                'buyer_name':wallet.wallet,
                'custom':'top up',
            }

            txn = paycoin.createTransaction(tx_para)
            print(txn)
            
            tc = TopupCard()
            tc.card = gt_card
            tc.from_user = request.user
            tc.identify_walletaddress = wallet.wallet
            tc.amount = int(amount)
            tc.payment_amount = pamt #amount+((0.75/100)*amount)
            tc.payment_type = 'coinpayment'
            tc.coinpayment_tx_hash = txn['txn_id']
            tc.payment_status = 'initiated'
            tc.save()

            return HttpResponseRedirect(txn['checkout_url'])
        else:
            return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/dashboard')


@login_required(login_url='/')
def getTransactionLog(request,card_no):
    if request.user.is_authenticated:
        res = card.transactions(card_no)
        print(res)
        if res['success']:
            return JsonResponse(res)
        else:
            print("Balance API Error")
            return HttpResponseBadRequest("API Error")
    else:
        return HttpResponseBadRequest("User Not Authenticated.")

@login_required(login_url='/')
def getCardTypeInfo(request,card_type):
    if request.user.is_authenticated:
        try:
            c = CardTypes.objects.get(card_type=card_type)
            res = {"card_generate_fee":c.card_generatefee,
                    "card_topup_fee":c.card_topup_fixfee,
                    "card_topup_per":c.card_topup_percentfee,
            }
            return JsonResponse(res)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Card not available")
    else:
        return HttpResponseBadRequest("User Not Authenticated.")


@login_required(login_url='/')
def exeUpdateUser(request):
    if request.user.is_authenticated and request.user.is_staff:
        import subprocess
        #pa = "Omkomg.1234"
        cmd2 = subprocess.Popen(['systemctl','--user','start','pythontest.service'])
        return HttpResponse(status=200)
    else:
        return HttpResponseBadRequest("User Not Authenticated.")