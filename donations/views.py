from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

from donations.models import *
# Create your views here.

def home(request):
    return render_to_response('donations/home.html', {
            'donor_total_count': Profile.objects.filter(is_donor=True).count(),
            'donee_total_count': Profile.objects.filter(is_donor=False).count(),
        }
    )

class DonorView(View):
    """ View for accessing/creating Donor """

    def get(self, request, *args, **kwargs):
        """ Render the new donor registration page """
        return render_to_response('donations/donor_signup.html')

    def post(self, request, *args, **kwargs):
        """ Create a new donor """

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        ref_id = request.POST['ref_id']

        u = User.objects.create_user(
            email, # username 
            email,
            email, # password
            first_name=first_name,
            last_name=last_name
        )

        p = Profile(
            user=u,
            is_donor=True,
            referrer=Profile.objects.get(registration_id=ref_id)
        )
        p.save()

        subject = "Welcome to HelpingHands"
        from_email = "webmaster@helpinghands.com"
        to = email
        
        context = {
            'name': first_name,
            'username': email,
            'password': email,
            'registration_id': p.registration_id,
        }
        msg_plain = render_to_string('donations/welcome_donor.txt', context)
        msg_html = render_to_string('donations/welcome_donor.html', context)
        
        msg = EmailMessage(subject, msg_html, from_email, [to])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        
        return HttpResponse('success')

