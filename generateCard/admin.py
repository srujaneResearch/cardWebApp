from django.contrib import admin
from generateCard.models import InitialPayment,CardTypes,TopupCard,CardGenerated
admin.site.register(InitialPayment)
admin.site.register(CardGenerated)
# Register your models here.
