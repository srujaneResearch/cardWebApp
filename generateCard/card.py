import requests
import mysql.connector
api_key = "asnaPm3ZbiNFPnVlbUk0BTV7LFe3mUW8w1Bh6l0gANMfSilArk65Fif8ZCXg"
base_url = "https://merchant.fcfpay.com/api"

def issueCard(name,surname,amount,address_l1,address_l2,city,state,country,zip,card_type,phone='38094098393',email='rakitnik@dolaso.ch'):
    payload={
        "iframe_id": 254,
        "surname": surname,
        "name": name,
        "amount": amount,
        "address_line1": address_l1,
        "address_line2": address_l2,
        "city": city,
        "state": state,
        "country":country,
        "zip":zip,
        "phone":2766818928,
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

def transactions(card_no):
    payload={
        "card_number": card_no,
    }
    headers={"Authorization":"Bearer "+api_key}
    r = requests.post(base_url+"/cards/get-card-transactions",data=payload,headers=headers)
    return r.json()


