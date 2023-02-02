
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.http import urlencode
# Create your views here.
from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import mysql.connector
from django.contrib.auth.models import User
from generateCard import card
from generateCard.models import CardGenerated,CardTypes,TopupCard,UserWallet,InitialPayment
from generateCard import forms
from django.views.decorators.csrf import csrf_exempt
from generateCard import pyCoinpayments
coin_pub = "d9c1815b8809bc4627561eda3a185528645f7bbe57ed97f94b3e8e1a78a03ca5"
coin_pvt = "F3Daf74154b0597Cf8cB69eEb0A782f85D0cdfE7a4644dAAdeD655987Ec27866"

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
        encoded_ = urlencode(request.POST).encode('utf-8')
        hashcode = hmac.new(bytearray('Soul1234', 'utf-8'), encoded_, hashlib.sha512).hexdigest()
        print("our hmac",hashcode)
        
        return HttpResponse(status=200)

    else:
        return HttpResponse(status=200)


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')    
    return render(request, 'generateCard/login.html')

def singup(request):
    return render(request,'generateCard/signup.html')

def register(request):
    if request.method == 'POST':
        email,password = request.POST['email'],request.POST['password']
        print(request.method)
        if len(accessUser(email)) != 0:
            user = User.objects.create_user(username=email,email=email,password=password)
            user.save()
            auser = authenticate(request,username=email,password=password)

            if auser is not None:
                login(request,auser)
                return HttpResponseRedirect('/dashboard')
            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
            
    else:
        return HttpResponseRedirect('/')

def loginAuth(request):
    #print(request.method,'\n\n',request)
    if request.method=='POST':
        print("login view")

        if request.user.is_authenticated:
            return HttpResponseRedirect('/dashboard')
        else:
            username,password = request.POST['email'],request.POST['password']
            user = authenticate(username=username,password=password)
            print(user)
            if user is not None:
                print("login complete")
                login(request,user)
                return HttpResponseRedirect('/dashboard')
            else:
                print("not")
                return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

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
    udb = accessUser(user.username)[0]
    print(udb)
    c = CardTypes.objects.all()
    cards_generated = CardGenerated.objects.filter(card_holder_user=request.user)
    if len(cards_generated)==0:
        card_status = False
    else:
        card_status=True
    cform = forms.GenerateCardForm()
    print(card_status)
    print(cards_generated)
    token_balance,wallet,emailaddr = int(udb[16]),udb[13],udb[2]
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
            name,surname,amount,addl1,addl2,city,state,country,zipcode,cardtype = request.POST['name'],request.POST['surname'],request.POST['amount'],request.POST['addl1'],request.POST['addl2'],request.POST['city'],request.POST['state'],request.POST['country'],request.POST['zipcode'],request.POST['cardtype']
            coin = request.POST['crypto']
            print(name)

            paycoin = pyCoinpayments.CryptoPayments(coin_pub,coin_pvt,'http://eternalcard.net/coinpaymentWebhook')
            
            pamt = (int(amount)*(0.75/100))+int(amount)
            
            tx_para = {
                'amount':pamt,
                'currency1':'USD',
                'currency2':coin,
                'buyer_email':request.user.email,
                'buyer_name':wallet
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
            return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/')
            

"""
@login_required(login_url='/')
def generateCardUSD(request):
    udb = accessUser(request.user.email)[0]
    token_bal,wallet = int(udb[16]),udb[13]
    if token_bal < 2499:
        HttpResponseRedirect('/dashboard')
    else:
        if request.method=='POST':
            print(request.POST)
            name,surname,amount,addl1,addl2,city,state,country,zipcode,cardtype = request.POST['name'],request.POST['surname'],request.POST['amount'],request.POST['addl1'],request.POST['addl2'],request.POST['city'],request.POST['state'],request.POST['country'],request.POST['zipcode'],request.POST['cardtype']
            print(name)
            res = card.issueCard(name,surname,amount,addl1,addl2,city,state,country,zipcode,cardtype)
            print(res)
            if res['success']:
                card_number,card_exm,card_exy,card_cvv,balance = int(res['message']['card_info']['card_number']),int(res['message']['card_info']['card_exp_mth']),int(res['message']['card_info']['card_exp_year']),int(res['message']['card_info']['card_cvv']),res['message']['card_balance']['balance']
                ct = CardTypes.objects.filter(card_type=cardtype)[0]
                c = CardGenerated()
                c.card_type = ct
                c.card_holder_user = request.user
                c.card_number = card_number
                c.identify_walletaddress = wallet
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
                c.initial_payment_id = InitialPayment.objects.all()[0]
                c.save()
                return HttpResponseRedirect('/dashboard')
            else:
                return HttpResponseRedirect('/dashboard')
        else:
            return HttpResponseRedirect('/dashboard')

            #res = card.issueCard()
        
"""