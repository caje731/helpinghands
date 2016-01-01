from __future__ import unicode_literals

from django.db import models
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
        on_delete=models.CASCADE
    )
    is_donor = models.BooleanField()
    address = models.OneToOneField(
        'Address',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
    )
    work = models.OneToOneField(
        'WorkDetail',
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
    )
    bank_details = models.OneToOneField(
        'BankDetail',
        on_delete=models.SET_NULL,
        null=True, # Donors will not enter bank details
        blank=True,
    )
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
    res_phone = models.CharField(
        verbose_name='Residence Phone',
        max_length=255,
        null=True, # Not everyone may have a residential phone
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
        
class Address(models.Model):
    """ Residential Address details for each user """

    house_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

class WorkDetail(models.Model):
    """ Workplace-related info """

    occupation = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    phone = models.CharField(verbose_name='Office Phone', max_length=255)
    email = models.EmailField(verbose_name='Office Email')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def user_dir_path(instance, filename):
    """ Return a string representing the full path to upload a file """
    
    # file will be uploaded to MEDIA_ROOT/uploads/user_<id>/<filename>
    return 'uploads/user_{0}/{1}'.format(instance.user.id, filename)

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
    cheque_copy = models.ImageField(max_length=255, upload_to=user_dir_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CaseDetail(models.Model):
    """ Information about a donee's case """

    REASON_CHOICES = (
        (1, 'Medical/Health'),
        (2, 'Education'),
        (3, 'Support due to loss of parent(s)'),
        (4, 'Other (please mention the reason)'),
    )

    CASE_STATUS_CHOICES = (
        (1, 'Registered'),
        (2, 'Under Verification'),
        (3, 'Verified'),
        (4, 'Rejected'),
        (5, 'Closed')
    )
    
    reason = models.PositiveSmallIntegerField(choices=REASON_CHOICES, default=1)
    reason_phrase = models.CharField(max_length=255, blank=True)
    brief = models.CharField(verbose_name="Brief of the case", max_length=255)
    status = models.PositiveSmallIntegerField(
        choices=CASE_STATUS_CHOICES,
        default=1
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
