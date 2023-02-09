from django.contrib import admin
from generateCard.models import InitialPayment,CardTypes,TopupCard,CardGenerated,UserWallet

class NewAdminSite(admin.AdminSite):
    site_header = "NewEternalLife"

class CardTypesAdmin(admin.ModelAdmin):
    list_display = ('card_type','card_name','card_currency')

class UserWalletAdmin(admin.ModelAdmin):
    list_display = ('user','wallet')

class CardGeneratedAdmin(admin.ModelAdmin):
    list_display=('card_type','card_holder_user','identify_walletaddress','card_number','card_balance')
    search_fields=['identify_walletaddress','card_type','card_holder_user']

class InitialPaymentAdmin(admin.ModelAdmin):
    list_display=('user','card_type','identify_walletaddress','payment_amount','payment_status','payment_type','card_holder_name')
    list_filter = ['payment_status','payment_type']
    search_fields=['identify_walletaddress','user','card_type']

class TopupAdmin(admin.ModelAdmin):
    list_display=('from_user','card','identify_walletaddress','payment_amount','payment_status','payment_type')
    list_filter = ['payment_status','payment_type']
    search_fields=['identify_walletaddress','from_user','card']

#a.register(InitialPayment,InitialPaymentAdmin)

admin.site.register(InitialPayment,InitialPaymentAdmin)
admin.site.register(CardGenerated,CardGeneratedAdmin)
admin.site.register(CardTypes,CardTypesAdmin)
admin.site.register(TopupCard,TopupAdmin)
admin.site.register(UserWallet,UserWalletAdmin)
#admin.site.register(CardGenerated)
# Register your models here.
