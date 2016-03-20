import django.contrib.admin as dca
from donations.models import *

# Register your models here.

class AddressInline(dca.StackedInline):
	model = Address

class ContactInline(dca.StackedInline):
	model = Contact

class WorkInline(dca.StackedInline):
	model = WorkDetail

class BankInline(dca.StackedInline):
	model = BankDetail


class CaseDetailAdmin(dca.ModelAdmin):
	inlines = [
		ContactInline,
		AddressInline,
		WorkInline,
		BankInline,
	]

dca.site.register(Profile)
dca.site.register(CaseDetail, CaseDetailAdmin)
