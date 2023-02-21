from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class CardTypes(models.Model):
    card_type = models.IntegerField()
    card_name = models.CharField(max_length=200)
    card_currency = models.CharField(max_length=6)
    card_generatefee = models.IntegerField()
    card_topup_fixfee = models.IntegerField()
    card_topup_percentfee = models.IntegerField()
    card_monthly_fee = models.FloatField()
    card_balance_limit = models.BigIntegerField()
    card_transaction_limit = models.BigIntegerField()
    card_kyc = models.BooleanField()

    def __str__(self):
        return str(self.card_name)

class UserWallet(models.Model):
    wallet = models.CharField(max_length=255,null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class InitialPayment(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    identify_walletaddress = models.CharField(max_length=255)
    amount = models.IntegerField(validators=[MinValueValidator(50),MaxValueValidator(5000)])
    payment_amount = models.FloatField()
    coinpayment_fees = models.FloatField(default=0.75)
    payment_type = models.CharField(max_length=12,choices=[('manual','manual'),
                                                            ('coinpayment','coinpayment')
                                                        ])
                                                            
    coinpayment_tx_hash = models.CharField(max_length=255,null=True,blank=True)
    payment_status = models.CharField(max_length=15,choices=[('initiated','initiated'),
                                                            ('rejected','rejected'),
                                                            ('successful','successful'),
                                                            ('approved','approved'),
                                                            ('pending','pending')])
    payed_from_wallet_address = models.CharField(max_length=255,null=True,blank=True)
    payed_transaction_hash = models.CharField(max_length=255,null=True,blank=True)
    card_type = models.ForeignKey(CardTypes,on_delete=models.CASCADE)
    card_holder_surname = models.CharField(max_length=40)
    card_holder_name = models.CharField(max_length=40)
    card_holder_addressline1 = models.TextField()
    card_holder_addressline2 = models.TextField()

    card_holder_city = models.CharField(max_length=30)
    card_holder_state = models.CharField(max_length=30)
    card_holder_country = models.CharField(max_length=50)
    card_holder_zip = models.IntegerField()
    timestamp_initiated = models.DateTimeField(auto_now_add=True,blank=True)
    timestamp_finished = models.DateTimeField(null=True,blank=True)

class CardGenerated(models.Model):
    card_type = models.ForeignKey(CardTypes,on_delete=models.CASCADE)
    card_holder_user = models.ForeignKey(User,on_delete=models.CASCADE)
    identify_walletaddress = models.CharField(max_length=255)
    card_holder_surname = models.CharField(max_length=40)
    card_holder_name = models.CharField(max_length=40)
    card_holder_addressline1 = models.TextField()
    card_holder_addressline2 = models.TextField()

    card_holder_city = models.CharField(max_length=30)
    card_holder_state = models.CharField(max_length=30)
    card_holder_country = models.CharField(max_length=50)
    card_holder_zip = models.IntegerField()
    card_number = models.BigIntegerField()
    card_expiry_month = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(12)])
    card_expiry_year = models.IntegerField()
    card_cvv = models.IntegerField()
    card_balance = models.IntegerField()
    initial_payment_id = models.ForeignKey(InitialPayment,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.card_number)



class TopupCard(models.Model):
    card = models.ForeignKey(CardGenerated,on_delete=models.CASCADE)
    from_user =  models.ForeignKey(User,on_delete=models.CASCADE)
    identify_walletaddress = models.CharField(max_length=255)

    amount = models.FloatField()
    payment_amount = models.FloatField()
    coinpayment_fees = models.FloatField(default=0.75)
    payment_type = models.CharField(max_length=12,choices=[('manual','manual'),
                                                            ('coinpayment','coinpayment')
                                                        ])
                                                            
    coinpayment_tx_hash = models.CharField(max_length=255,null=True,blank=True)
    payment_status = models.CharField(max_length=15,choices=[('initiated','initiated'),
                                                            ('rejected','rejected'),
                                                            ('successful','successful'),
                                                            ('approved','approved'),
                                                            ('pending','pending')])
    payed_from_wallet_address = models.CharField(max_length=255,null=True,blank=True)
    payed_transaction_hash = models.CharField(max_length=255,null=True,blank=True)
    timestamp_initiated = models.DateTimeField(auto_now_add=True)
    timestamp_finished = models.DateTimeField(null=True,blank=True)

class AuthTokens(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_requested = models.DateTimeField()
    expiry = models.DateTimeField()
    status = models.BooleanField()
    token =  models.CharField(max_length=255)

class TwoFAAuth(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    date_requested = models.DateTimeField()
    expiry = models.DateTimeField()
    status = models.BooleanField()
    token = models.CharField(max_length=255)
    otp = models.IntegerField()
    attempt = models.IntegerField()
    block = models.BooleanField(default=False)
    block_time_over = models.DateTimeField(blank=True,null=True)


# Create your models here.
