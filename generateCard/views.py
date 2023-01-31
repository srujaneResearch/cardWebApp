
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import mysql.connector
from django.contrib.auth.models import User
from generateCard import card
from generateCard.models import CardGenerated,CardTypes,TopupCard,UserWallet,InitialPayment
from generateCard import forms
def accessUser(email):
    db = mysql.connector.connect(host="server07.hostfactory.ch",user="card_wepapp",password="E9ytaGuMAtAMuBUh",database="Token")

    cur = db.cursor()
    cur.execute("select * from users where email='{0}'".format(email))
    l = cur.fetchall()

    return l


def index(request):    
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
    context = {'tokenBalance':token_balance,
                'wallet':wallet,
                'emailaddress':emailaddr,
                'cardTypes':c,
                'card_status':card_status,
                "cardgenerated":cards_generated,
                "cform":cform
    }
    return render(request,'generateCard/dashboard.html',context)

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
        
