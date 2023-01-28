from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from django.template import loader
#from addWallet.models import wallets
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import mysql.connector
from django.contrib.auth.models import User


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

    token_balance,wallet = udb[16],udb[13]
    context = {'tokenBalance':token_balance}
    return render(request,'generateCard/dashboard.html',context)



