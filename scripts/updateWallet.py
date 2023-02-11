
from generateCard.models import UserWallet
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

import mysql.connector


def accessUser():
    db = mysql.connector.connect(host="server07.hostfactory.ch",user="card_wepapp",password="E9ytaGuMAtAMuBUh",database="Token")

    cur = db.cursor()
    cur.execute("select * from users")
    l = cur.fetchall()

    return l


def checkWallet(wallet):
    try:
        if User.objects.get(userwallet__wallet=wallet):
            return True
    except:
        return False
    

def run():
    ico_user = accessUser()
    ico_email = [x[2] for x in ico_user]
    ico_wallet = [x[13] for x in ico_user]
    web_user = User.objects.all()


    for i_u in range(len(ico_wallet)):
        print("At ",ico_email[i_u])
        if i_u == None:
            print("Wallet is none")
            guser = web_user.get(email=ico_email[i_u])
            if guser.userwallet.wallet == None:
                guser.userwallet.save()
                continue
            else:
                guser.userwallet.wallet=None
                guser.userwallet.save()
                guser.initialpayment_set.update(identify_walletaddress=None)
                guser.cardgenerated_set.update(identify_walletaddress=None)
                guser.topupcard_set.update(identify_walletaddress=None)
                guser.save()
                continue
        if not checkWallet(i_u):
            #print(i_u)
            try:
                guser = web_user.get(email=ico_email[i_u])
                guser.userwallet.wallet=ico_wallet[i_u]
                guser.userwallet.save()
                guser.initialpayment_set.update(identify_walletaddress=ico_wallet[i_u])
                guser.cardgenerated_set.update(identify_walletaddress=ico_wallet[i_u])
                guser.topupcard_set.update(identify_walletaddress=ico_wallet[i_u])
                guser.save()
            except ObjectDoesNotExist:
                print("object doesnot exsist")

