print("hello")



from generateCard.models import UserWallet
from django.contrib.auth.models import User

import mysql.connector

def accessUser(email):
    db = mysql.connector.connect(host="server07.hostfactory.ch",user="card_wepapp",password="E9ytaGuMAtAMuBUh",database="Token")

    cur = db.cursor()
    cur.execute("select * from users where email='{0}'".format(email))
    l = cur.fetchall()

    return l

def run():
    user_wallet = UserWallet.objects.all()
    u_have = [x.user for x in user_wallet]

    auth_u = User.objects.all()
    print(u_have,"\n")
    for i in auth_u:
        if i not in u_have:
            print("not in user wallet",i)
            new_user = UserWallet()
            new_user.user = i
            try:
                wlt = accessUser(i.email)[0][13]
                print(wlt)
                if wlt != None:
                        
                    new_user.wallet = wlt
                    new_user.save()
                    print("usr saved")
                else:
                    new_user.wallet = None
                    new_user.save()
                    print("usr saved")
                    #print("wallet not gound")
            except:
                print("Major error")
                continue
