
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
    web_user = User.objects.all()
    w_email = [ x.email for x in web_user]


    for i_u in ico_email:
        if i_u not in w_email:
            print(i_u)
            new_user = User.objects.create_user(username=i_u,email=i_u,password="")
            new_user.is_active = False
            new_user.save()
            u = UserWallet()
            u.user = new_user
            u.wallet = ico_wallet[ico_email.index(i_u)]
            u.save()
