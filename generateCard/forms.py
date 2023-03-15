from django import forms
from generateCard.models import CardTypes
from django.core.validators import RegexValidator
from generateCard import countrylist_new


class TopupForm(forms.Form):
    Amount = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Min $50 Max- $5000'}))
    topupfix = forms.CharField(required=True,label="Topup fee",widget=forms.TextInput(attrs={'placeholder': 'Topup fee'}),disabled=True)
    topupper = forms.CharField(required=True,label="Topup % fee",widget=forms.TextInput(attrs={'placeholder': 'Topup % fee'}),disabled=True)
    totaltfee = forms.CharField(required=True,label="Total fee",widget=forms.TextInput(attrs={'placeholder': 'Total fee'}),disabled=True)
    crypto = forms.ChoiceField(choices=[('BTC','Bitcoin'),
                                        ('ETH','Ethereum'),
                                        ('ETC','Ether Classic'),
                                        ('BNB.BSC','BNB Coin'),
                                        ('LTC','Litecoin'),
                                        ('USDT.TRC20','Tether USD'),
                                        ('TRX','TRON'),
                                        #('LTCT','Litecoin Test')
                                        ])
    cpay = forms.CharField(required=True,label="coinpament fee",widget=forms.TextInput(attrs={'placeholder': '0.75% coinpayment fee'}),disabled=True)

class GenerateCardForm(forms.Form):
    c = [(x.card_type,x.card_name) for x in CardTypes.objects.all()]
    cardtype = forms.ChoiceField(choices=c)
    amount = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Min $50 Max - $5000'}))
    cgenfee = forms.CharField(required=True,label="Card generate fee",widget=forms.TextInput(attrs={'placeholder': 'card generate fee'}),disabled=True)
    topfix = forms.CharField(required=True,label="Topup fee",widget=forms.TextInput(attrs={'placeholder': 'Topup fix fee'}),disabled=True)
    topper = forms.CharField(required=True,label="Topup % fee",widget=forms.TextInput(attrs={'placeholder': 'Topup \% fee'}),disabled=True)
    totalfee = forms.CharField(required=True,label="Total fee",widget=forms.TextInput(attrs={'placeholder': 'Total fee'}),disabled=True)
    name = forms.CharField(max_length=255, required=True,widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    surname = forms.CharField(max_length=255, required=True,widget=forms.TextInput(attrs={'placeholder': 'Surname'}))
    addl1 = forms.CharField(widget=forms.Textarea,required=True, label="Street and house no.")
    zipcode = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=255, required=True)
    state = forms.CharField(max_length=255, required=True,label="Province")
    cntry = countrylist_new.country
    country = forms.ChoiceField(choices=[(x['country-code'],x['name']) for x in cntry] )

    crypto = forms.ChoiceField(choices=[('BTC','Bitcoin'),
                                        ('ETH','Ethereum'),
                                        ('ETC','Ether Classic'),
                                        ('BNB.BSC','BNB Coin'),
                                        ('LTC','Litecoin'),
                                        ('USDT.TRC20','Tether USD'),
                                        ('TRX','TRON'),
                                        #('LTCT','Litecoin Test')
                                        ])
    cpayg = forms.CharField(required=True,label="coinpament fee",widget=forms.TextInput(attrs={'placeholder': '0.75% coinpayment fee'}),disabled=True)
