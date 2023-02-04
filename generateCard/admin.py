from django.contrib import admin
from generateCard.models import InitialPayment,CardTypes,TopupCard,CardGenerated,UserWallet
admin.site.register(InitialPayment)
admin.site.register(CardGenerated)
admin.site.register(CardTypes)
admin.site.register(TopupCard)
admin.site.register(UserWallet)
#admin.site.register(CardGenerated)
# Register your models here.
