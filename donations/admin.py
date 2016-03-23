import django.contrib.admin as dca
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
                

dca.site.register(Profile)
dca.site.register(CaseDetail, CaseDetailAdmin)
