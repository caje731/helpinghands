""" Views for my precious """

import json

from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, QueryDict
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from donations.models import Profile
# Create your views here.

def home(request):
    """ Show the home page """

    return render(
        request,
        'donations/nav_bar/home.html',
        {
            'donor_total_count': Profile.objects.filter(is_donor=True).count(),
            'donee_total_count': Profile.objects.filter(is_donor=False).count(),
        },
    )

def logout_view(request):
    """ Logout the current user and redirect to the home page """
    logout(request)
    # Redirect to a success page.

    return home(request)

class DonorSignupView(View):
    """ View for accessing/creating Donor """

    def get(self, request, *args, **kwargs):
        """ Show the donor registration page """

        return render(
            request,
            'donations/donor/signup.html'
        )

    def post(self, request, *args, **kwargs):
        """ Create a new donor """

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        ref_id = request.POST['ref_id']
        phone =  request.POST['phone']

        referrer = None
        try:
            referrer = Profile.objects.get(registration_id=ref_id)
        except Profile.DoesNotExist:
            return JsonResponse(
                {
                    'status': 'failure',
                    'message': 'Referrer ID is invalid'
                },
                status=400,
            )

        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {
                    'status': 'failure',
                    'message': 'A profile with the same email already exists'
                },
                status=400,
            )

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
            referrer=referrer,
            cell_phone=phone,
        )
        p.save()

        subject = "Welcome to HelpingHands"
        from_email = "www.helpinghands.gives<webmaster@helpinghands.gives>"
        to_email = email
        
        context = {
            'name': first_name,
            'username': email,
            'password': email,
            'registration_id': p.registration_id,
        }
        msg_plain = render_to_string(
            'donations/email/welcome_donor.txt',
            context
        )
        msg_html = render_to_string(
            'donations/email/welcome_donor.html',
            context
        )

        msg = EmailMultiAlternatives(subject, msg_plain, from_email, [to_email])
        msg.attach_alternative(msg_html, "text/html")
        msg.send()
        
        return JsonResponse(
            {
                'status': 'success',
                'message': 'Profile successfully created'
            }
        )

class ProfileView(LoginRequiredMixin, View):
    login_url = "/accounts/login/"

    def get(self, request, *args, **kwargs):
        if request.user.profile.is_donor:
            return render(
                request,
                'donations/donor/logged_in.html',
            )

    def patch(self, request, *args, **kwargs):
        """ Update user details """

        data = QueryDict(request.body)

        first_name = data['first_name']
        last_name = data['last_name']
        phone =  data['phone']

        if first_name is not None and len(first_name) > 0:
            if request.user.first_name != first_name:
                request.user.first_name = first_name
                request.user.save()
        else:
            return JsonResponse(
                {
                    'status': 'failure',
                    'message': 'First Name cannot be blank'
                },
                status=400,
            )

        if last_name is not None and len(last_name) > 0:
            if request.user.last_name != last_name:
                request.user.last_name = last_name
                request.user.save()
        else:
            return JsonResponse(
                {
                    'status': 'failure',
                    'message': 'Last Name cannot be blank'
                },
                status=400,
            )

        if phone is not None and len(phone) > 0:
            if request.user.profile.cell_phone != phone:
                request.user.profile.cell_phone = phone
                request.user.profile.save()
        
        return JsonResponse(
            {
                'status': 'success',
                'message': 'Profile successfully updated'
            }
        )
