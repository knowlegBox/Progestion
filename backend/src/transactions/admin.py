from django.contrib import admin

from transactions.models import Versement


# Register your models here.

@admin.register(Versement)
class DepotAdmin(admin.ModelAdmin):
    pass


# @admin.register(Facture)
# class WithdrawalAdmin(admin.ModelAdmin):
#     pass
