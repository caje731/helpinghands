from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum
from helpinghands import settings

import os, datetime, binascii
# Create your models here.

class Profile(models.Model):
    """ Extension of the auth.User model """

    registration_id = models.CharField(
        'Registration ID',
        max_length=255,
        unique=True,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True
    )
    is_donor = models.BooleanField()
    referrer = models.ForeignKey(
        'self',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
    )
    cell_phone = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    case_details = models.OneToOneField(
        'CaseDetail',
        on_delete=models.SET_NULL,
        null=True, # Cases only belong to donees
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """ Override the save method to update the registration_id """

        if self.registration_id is None or self.registration_id == '':
            today = datetime.date.today().strftime('%Y%m%d')
            prefix = 'R'
            if self.is_donor:
                prefix = 'D'        
            self.registration_id = prefix + today + binascii.hexlify(os.urandom(3))

        # Call the "real" save() method.
        super(Profile, self).save(*args, **kwargs) 
        
class Contact(models.Model):
    """ Contact details for each case """

    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    phone_2 = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    email = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    case = models.OneToOneField(
        'CaseDetail',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Address(models.Model):
    """ Details of residential address """
    house_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    case = models.OneToOneField(
        'CaseDetail',
        on_delete=models.CASCADE,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

class WorkDetail(models.Model):
    """ Workplace-related info """

    occupation = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    phone = models.CharField(verbose_name='Office Phone', max_length=255)
    email = models.EmailField(verbose_name='Office Email')
    case = models.OneToOneField(
        'CaseDetail',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def user_dir_path(instance, filename):
    """ Return a string representing the full path to upload a file """
    
    # file will be uploaded to MEDIA_ROOT/uploads/user_<id>/<filename>
    return 'uploads/user_{0}/{1}'.format(instance.user.id, filename)

def cheque_copy_upload_path(instance, filename):
    """ Return an upload path for documents of BankDetail instance """
    # file will be uploaded to MEDIA_ROOT/uploads/cases/<case_id>/bank/<filename>
    return 'uploads/cases/{0}/bank/{1}'.format(instance.case.id, filename)

class BankDetail(models.Model):
    """ Bank Account information """
    acc_holder_name = models.CharField(
        verbose_name="Account Holder's Name",
        max_length=255
    )
    acc_number = models.CharField(verbose_name='Account Number', max_length=255)
    bank_name = models.CharField(max_length=255)
    branch_name = models.CharField(max_length=255)
    ifsc = models.CharField(verbose_name='IFSC', max_length=11)
    cheque_copy = models.ImageField(max_length=255, upload_to=cheque_copy_upload_path)
    case = models.OneToOneField(
        'CaseDetail',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CaseDetail(models.Model):
    """ Information about a donee's case """

    REASON_CHOICES = (
        (1, 'Medical'),
        (2, 'Basic Education'),
    )

    CASE_STATUS_CHOICES = (
        (1, 'Registered'),
        (2, 'Under Verification'),
        (3, 'Verified'),
        (4, 'Rejected'),
        (5, 'Closed')
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    reason = models.PositiveSmallIntegerField(choices=REASON_CHOICES, default=1)
    brief = models.TextField(verbose_name="Short Description")
    wish_amount = models.FloatField(default=0)
    approved_amount = models.FloatField(default=0)
    status = models.PositiveSmallIntegerField(
        choices=CASE_STATUS_CHOICES,
        default=1
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def pledge_total(self, user=None):
        """ Get the total amount pledged for this case """
        if user is not None:
            return CasePledge.objects.filter(case=self, user=user).aggregate(Sum('amount'))
        return CasePledge.objects.filter(case=self).aggregate(Sum('amount'))


class CasePledge(models.Model):
    """ All pledges for a case """
    amount = models.FloatField(default=0)
    case = models.ForeignKey(CaseDetail)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    remitted = models.BooleanField(default=False)
    txn_ref = models.TextField(verbose_name="Transaction Details", default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Approval(models.Model):
    """ Approval for a case """
    approved = models.BooleanField()
    approver = models.ForeignKey('Profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# I'd have liked this function to be inside the ApprovalAttachment class
# body, however see the section on what Django can(not) serialize:
# https://docs.djangoproject.com/en/1.9/topics/migrations/#serializing-values
def approvalattachment_upload_path(instance, filename):
    """ Return an upload path for approval-related documents """
    # file will be uploaded to (MEDIA_ROOT + below)
    return 'uploads/cases/{0}/approvals/{1}/{2}'.format(
        instance.attached_for.case.id,
        instance.attached_for.id,
        filename
    )

class ApprovalAttachment(models.Model):
    """ Files to be uploaded in support of approvals """

    attachment = models.ImageField(
        max_length=255,
        upload_to=approvalattachment_upload_path
    )
    attached_for = models.ForeignKey(
        Approval,
        on_delete=models.CASCADE,
        null=True, # Allow creation of attachments without an Approval instance
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PhoneApproval(Approval):
    """ Approval after a phone conversation with recipient """
    case = models.OneToOneField(
        'CaseDetail',
        on_delete=models.CASCADE,
    )

class PersonalInterviewApproval(Approval):
    """ Approval after a personal interview with recipient """
    case = models.OneToOneField(
        'CaseDetail',
        on_delete=models.CASCADE,
    )

class VisitApproval(Approval):
    """ Approval after a visit to residence/office of recipient """
    case = models.OneToOneField(
        'CaseDetail',
        on_delete=models.CASCADE,
    )

def remitproof_upload_path(instance, filename):
    """ Return an upload path for remittance proofs """
    return 'uploads/cases/{0}/pledges/{1}/{2}'.format(
        instance.pledge.case.id,
        instance.pledge.id,
        filename
    )

class RemittanceProof(models.Model):
    """ Proof attachments for donors remitting against their pledges """

    attachment = models.ImageField(
        max_length=255,
        upload_to=remitproof_upload_path
    )
    pledge = models.ForeignKey(CasePledge)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
