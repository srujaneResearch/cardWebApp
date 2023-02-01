from django import forms
from generateCard.models import CardTypes
from django.core.validators import RegexValidator

class GenerateCardForm(forms.Form):
    name = forms.CharField(max_length=255, required=True,)
    surname = forms.CharField(max_length=255, required=True)
    amount = forms.CharField(required=True)
    addl1 = forms.CharField(widget=forms.Textarea,required=True)
    addl2 = forms.CharField(widget=forms.Textarea,required=True)
    city = forms.CharField(max_length=255, required=True)
    state = forms.CharField(max_length=255, required=True)
    country = forms.CharField(max_length=255, required=True)
    zipcode = forms.CharField(max_length=255, required=True)
    c = [(x.card_type,x.card_name) for x in CardTypes.objects.all()]
    cardtype = forms.ChoiceField(choices=c)
    crypto = forms.ChoiceField(choices=[('BTC','Bitcoin'),
                                        ('ETH','Ethereum'),
                                        ('ETC','Ether Classic'),
                                        ('BNB.BSC','BNB Coin'),
                                        ('LTC','Litecoin'),
                                        ('USDT.TRC20','Tether USD'),
                                        ('TRX','TRON')])


