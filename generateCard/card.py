import requests
import mysql.connector
api_key = "5v6kEHuFS0iaRrXuE8ZTF4jLxDv9BtEMpdlXk967tf7MZi8YnpodsjKgmh7q"
base_url = "https://sandbox.fcfpay.com/api"

def issueCard(name,surname,amount,address_l1,address_l2,city,state,country,zip,card_type,phone='38094098393',email='rakitnik@dolaso.ch'):
    payload={
        "iframe_id": 31,
        "surname": surname,
        "name": name,
        "amount": amount,
        "address_line1": address_l1,
        "address_line2": address_l2,
        "city": city,
        "state": state,
        "country":country,
        "zip":zip,
        "phone":"38094098393",
        "email":"rakitnik@dolaso.ch",
        "card_type": card_type,
        }
    headers={"Authorization":"Bearer "+api_key}

    r = requests.post(base_url+"/cards/issue-card-api",data=payload,headers=headers)
    return r.json()

def getBalance(card_no):
    payload = {
        "card_number": card_no
    }
    headers={"Authorization":"Bearer "+api_key}

    r = requests.post(base_url+"/cards/get-card-balance",data=payload,headers=headers)

    return r.json()

def topUpCard(amount,card_no):
    payload={
        "card_number": card_no,
        "amount": amount
    }
    headers={"Authorization":"Bearer "+api_key}
    r = requests.post(base_url+"/cards/load-virtual-card",data=payload,headers=headers)
    return r.json()

