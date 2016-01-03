""" Views for my precious """

from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from donations.models import Profile
# Create your views here.

def home(request):
    """ Show the home page """

    return render(
        request,
        'donations/home.html',
        {
            'donor_total_count': Profile.objects.filter(is_donor=True).count(),
            'donee_total_count': Profile.objects.filter(is_donor=False).count(),
        },
    )

class DonorView(View):
    """ View for accessing/creating Donor """

    def get(self, request, *args, **kwargs):
        """ Show the donor registration page """

        return render(
            request,
            'donations/donor_signup.html'
        )

    def post(self, request, *args, **kwargs):
        """ Create a new donor """

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        ref_id = request.POST['ref_id']
        phone =  request.POST['phone']

        usr = User.objects.create_user(
            email, # username 
            email,
            email, # password
            first_name=first_name,
            last_name=last_name
        )

        p = Profile(
            user=usr,
            is_donor=True,
            referrer=Profile.objects.get(registration_id=ref_id),
            cell_phone=phone,
        )
        p.save()

        subject = "Welcome to HelpingHands"
        from_email = "webmaster@helpinghands.com"
        to_email = email
        
        context = {
            'name': first_name,
            'username': email,
            'password': email,
            'registration_id': p.registration_id,
        }
        msg_plain = render_to_string('donations/welcome_donor.txt', context)
        msg_html = render_to_string('donations/welcome_donor.html', context)
        
        msg = EmailMultiAlternatives(subject, msg_plain, from_email, [to_email])
        msg.attach_alternative(msg_html, "text/html")
        msg.send()
        
        return HttpResponse('success')

