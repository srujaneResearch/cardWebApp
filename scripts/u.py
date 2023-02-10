print("hello")



from generateCard.models import UserWallet
from django.contrib.auth.models import User

import mysql.connector

def accessUser():
    db = mysql.connector.connect(host="server07.hostfactory.ch",user="card_wepapp",password="E9ytaGuMAtAMuBUh",database="Token")

    cur = db.cursor()
    cur.execute("select * from users")
    l = cur.fetchall()

    return l

def run():
    ico_user = accessUser()
    ico_email = [x[2] for x in ico_user]
    ico_wallet = [x[13] for x in ico_user]

    already = UserWallet.objects.all()

    auth_u = User.objects.all()
    for i in auth_u:
        if i.email not in ico_email:
            print(i)
            n_u = UserWallet()
            n_u.user = i
            n_u.wallet = None
            n_u.save()
            print("Saved")

