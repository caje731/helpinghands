import django.contrib.admin as dca
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from donations.models import *
import nested_admin

# Register your models here.

class AddressInline(dca.StackedInline):
    model = Address

class ContactInline(dca.StackedInline):
    model = Contact

class WorkInline(dca.StackedInline):
    model = WorkDetail

class BankInline(dca.StackedInline):
    model = BankDetail

class ApprovalAttachmentInline(nested_admin.NestedStackedInline):
    model = ApprovalAttachment
    extra = 1

class PhoneApprovalInline(nested_admin.NestedStackedInline):
    model = PhoneApproval
    exclude = ('approver',)
    inlines = [
        ApprovalAttachmentInline,
    ]
    def save_model(self, request, obj, form, change):
        obj.approver = request.user
        obj.save()

class VisitApprovalInline(nested_admin.NestedStackedInline):
    model = VisitApproval
    exclude = ('approver',)
    inlines = [
        ApprovalAttachmentInline,
    ]
    def save_model(self, request, obj, form, change):
        obj.approver = request.user
        obj.save()

class PersonalInterviewApprovalInline(nested_admin.NestedStackedInline):
    model = PersonalInterviewApproval
    exclude = ('approver',)
    inlines = [
        ApprovalAttachmentInline,
    ]
    def save_model(self, request, obj, form, change):
        obj.approver = request.user
        obj.save()

class CaseDetailAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        ContactInline,
        AddressInline,
        WorkInline,
        BankInline,
        PhoneApprovalInline,
        VisitApprovalInline,
        PersonalInterviewApprovalInline,
    ]

    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            instances = formset.save(commit=False)

            for instance in instances:
                if formset.__class__.__name__ in [
                    'PhoneApprovalFormFormSet',
                    'VisitApprovalFormFormSet',
                    'PersonalInterviewApprovalFormFormSet'
                ]:
                    instance.approver = request.user.profile
                
                instance.save()
            formset.save_m2m()
                
class CustomUserAdmin(UserAdmin):

    list_display = (
        'date_joined',
        'email',
        'first_name',
        'last_name',
        'referrer',
        'last_login',
        'is_staff',
    )

    def referrer(self, user_obj):
        """The name of this User's referrer"""
        
        refr = user_obj.profile.referrer
        return " ".join(
            [
                refr.user.first_name,
                refr.user.last_name,
            ]
        ) if refr else ""

    referrer.admin_order_field = 'profile__referrer__user'

dca.site.register(Profile)
dca.site.register(CaseDetail, CaseDetailAdmin)
dca.site.unregister(User)
dca.site.register(User, CustomUserAdmin)
