""" Views for my precious """

from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, QueryDict
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from donations.models import *
# Create your views here.

def home(request):
    """ Show the home page """
    current_case = list(CaseDetail.objects.filter(status=3).order_by('-id'))[-1]
    current_case_pledges = current_case.casepledge_set.aggregate(sum=Sum('amount'))['sum'] or 0 if current_case else 0
    current_case_remits = current_case.casepledge_set.filter(remitted=True).aggregate(sum=Sum('amount'))['sum'] or 0 if current_case else 0
    current_case_target_left = (current_case.approved_amount - current_case_pledges) if current_case else 0
    return render(
        request,
        'donations/nav_bar/home.html',
        {
            'donor_total_count': Profile.objects.filter(is_donor=True).count(),
            'donee_total_count': CaseDetail.objects.all().count(),
            'donee_rejected_count': CaseDetail.objects.filter(status=4).count(),
            'donee_under_verification_count':CaseDetail.objects.filter(status=2).count(),
            'donee_inprogress_count': CaseDetail.objects.filter(status=3).count(),
            'donee_closed_count': CaseDetail.objects.filter(status=5).count(),
            'current_case': current_case,
            'current_case_pledges': current_case_pledges,
            'current_case_remits': current_case_remits,
            'current_case_target_left': current_case_target_left,
            'total_donation': int(CasePledge.objects.filter(remitted=True).aggregate(Sum('amount'))['amount__sum'] or 0),
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

@login_required
def create_case(request):
    if request.method == 'POST':
        data = request.POST

        case = CaseDetail.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            reason=data['reason'],
            brief=data['brief'],
            wish_amount=data['wish_amt'],
        )

        address = Address.objects.create(
            house_name=data['house_name'],
            street=data['street'],
            area=data['area'],
            city=data['city'],
            state=data['state'],
            country=data['country'],
            pincode=data['pin'] or 0,
            case=case,
        )
        contact = Contact.objects.create(
            phone=data['phone'],
            email=data['email'],
            case=case
        )
        bank_acc = BankDetail.objects.create(
            acc_holder_name=data['acc_holder_name'],
            acc_number=data['acc_number'],
            bank_name=data['bank_name'],
            branch_name=data['branch_name'],
            ifsc=data['ifsc'],
            case=case
        )

        return JsonResponse(
            {
                'status':'success',
                'message': 'Case Created Successfully'
            },
            status=201
        )

    else:
        return HttpResponse(
            content="Method Not Allowed",
            status=405,
            reason="Attempting to use "+request.method+" with a POST-only endpoint"
        )

class DoneeSignupView(View):
    """ View for accessing/creating Donee """

    def get(self, request, *args, **kwargs):
        """ Show the donee registration page """

        return render(
            request,
            'donations/donee/signup.html'
        )

    def post(self, request, *args, **kwargs):
        """ Create a new donee """

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        ref_id = request.POST['ref_id']
        phone =  request.POST['phone']

        referrer = None
        try:
            referrer = Profile.objects.get(registration_id=ref_id)
            if referrer.registration_id[0] != 'D':
                # Referrer is not a Donor - don't allow registration
                return JsonResponse(
                    {
                        'status': 'failure',
                        'message': 'Referrer ID is invalid'
                    },
                    status=400,
                )
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
            is_donor=False,
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
            'donations/email/welcome_donee.txt',
            context
        )
        msg_html = render_to_string(
            'donations/email/welcome_donee.html',
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
        context = {
            'REASON_CHOICES': CaseDetail.REASON_CHOICES,
            'STATUS_CHOICES': CaseDetail.CASE_STATUS_CHOICES,
            'request': request,
            'cases_page': request.GET.get('page') or 1
        }
        if request.user.profile.is_donor:
            return render(
                request,
                'donations/donor/logged_in.html',
                context,
            )
        else:
            return render(
                request,
                'donations/donee/logged_in.html',
                context,
            )

    def patch(self, request, *args, **kwargs):
        """ Update user details """

        data = QueryDict(request.body)

        if data['patch_type'] == 'address':
            pass
        elif data['patch_type'] == 'work':
            pass
        elif data['patch_type'] == 'bank':
            acc_holder_name = data['acc_holder_name']
            acc_number = data['acc_number']
            bank_name = data['bank_name']
            branch_name = data['branch_name']
            ifsc = data['ifsc']
            cheque_copy = data['cheque_copy'] if 'cheque_copy' in data else None
            bank_acc = request.user.profile.bank_details

            if bank_acc is None:
                bank_acc = BankDetail()

            if acc_holder_name is not None and len(acc_holder_name) > 0:
                bank_acc.acc_holder_name = acc_holder_name
                bank_acc.save()
            else:
                return JsonResponse(
                    {
                        'status': 'failure',
                        'message': 'Account Holder Name cannot be blank'
                    },
                    status=400,
                )

            if acc_number is not None and len(acc_number) > 0:
                bank_acc.acc_number = acc_number
                bank_acc.save()
            else:
                return JsonResponse(
                    {
                        'status': 'failure',
                        'message': 'Account Number cannot be blank'
                    },
                    status=400,
                )

            if bank_name is not None and len(bank_name) > 0:
                bank_acc.bank_name = bank_name
                bank_acc.save()
            else:
                return JsonResponse(
                    {
                        'status': 'failure',
                        'message': 'Bank Name cannot be blank'
                    },
                    status=400,
                )

            if branch_name is not None and len(branch_name) > 0:
                bank_acc.branch_name = branch_name
                bank_acc.save()
            else:
                return JsonResponse(
                    {
                        'status': 'failure',
                        'message': 'Branch Name cannot be blank'
                    },
                    status=400,
                )

            if ifsc is not None and len(ifsc) > 0:
                bank_acc.ifsc = ifsc
                bank_acc.save()
            else:
                return JsonResponse(
                    {
                        'status': 'failure',
                        'message': 'IFSC cannot be blank'
                    },
                    status=400,
                )

            if cheque_copy is not None and len(cheque_copy) > 0:
                bank_acc.cheque_copy = cheque_copy
                bank_acc.save()
            request.user.profile.bank_details = bank_acc
            request.user.profile.save()

        elif data['patch_type'] == 'case':

            reason = data['reason']
            brief = data['brief']
            wish_amt = data['wish_amt']
            case = request.user.profile.case_details
            
            if case is None:
                case = CaseDetail()
            
            if reason is not None and reason != '':
                case.reason = reason
                case.save()
            else:
                return JsonResponse(
                    {
                        'status': 'failure',
                        'message': 'Reason not selected / invalid'
                    },
                    status=400,
                )

            if brief is not None and len(brief) > 0:
                case.brief = brief
                case.save()
            else:
                return JsonResponse(
                    {
                        'status': 'failure',
                        'message': 'Enter a short description for the case'
                    },
                    status=400,
                )                
            
            if wish_amt is not None and wish_amt != '' and float(wish_amt) > 0:
                case.wish_amount = float(wish_amt)
                case.save()
            else:
                return JsonResponse(
                    {
                        'status': 'failure',
                        'message': 'Amount must be greater than zero'
                    },
                    status=400,
                )
            request.user.profile.case_details = case
            request.user.profile.save()

        else:
            first_name = data['first_name']
            last_name = data['last_name']
            phone = data['phone']

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

class PaginatedCasesView(LoginRequiredMixin, View):
    """ View for accessing cases in a paginated manner """

    def get(self, request, *args, **kwargs):
        """ Get all cases """
        cases = CaseDetail.objects.filter(status=3)
        paginator = Paginator(cases, 1) # Show 1 case per page

        page = request.GET.get('page')
        try:
            paged_cases = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paged_cases = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            paged_cases = paginator.page(paginator.num_pages)

        return render(
            request,
            'donations/donor/cases.html',
            {
                'pledges': CasePledge.objects.filter(user=request.user, case__in=paged_cases),
                'cases': paged_cases,
                'STATUS_CHOICES': CaseDetail.CASE_STATUS_CHOICES,
                'REASON_CHOICES': CaseDetail.REASON_CHOICES,
            }
        )

class CasePledgesView(LoginRequiredMixin, View):
    """ View for accessing pledges of a case """

    def post(self, request, *args, **kwargs):
        """ Update pledge information for a case """
        try:
            user = request.user
            pledge_amount = abs(float(request.POST['pledge_amt']))
            case = CaseDetail.objects.get(pk=kwargs['id'])
            target_remaining = case.approved_amount - (case.casepledge_set.aggregate(sum=Sum('amount'))['sum'] or 0)
            case_pledge, created = CasePledge.objects.update_or_create(
                case=case,
                user=user,
                defaults={'amount': min(
                        target_remaining,
                        pledge_amount
                    )
                }
            )

            if created:
                # This was a new pledge so send account info to the donor 
                subject = "You've pledged to help "+ " ".join([case.first_name, case.last_name])
                from_email = "www.helpinghands.gives<webmaster@helpinghands.gives>"
                to_email = user.email
                
                context = {
                    'user': user,
                    'case': case,
                }
                msg_plain = render_to_string(
                    'donations/email/bank_details.txt',
                    context
                )
                msg_html = render_to_string(
                    'donations/email/bank_details.html',
                    context
                )

                msg = EmailMultiAlternatives(subject, msg_plain, from_email, [to_email])
                msg.attach_alternative(msg_html, "text/html")
                msg.send()
                
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Pledge saved successfully'
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    'status': 'failure',
                    'message': 'Something went wrong!',
                },
                status=500
            )

class PledgeRemittancesView(LoginRequiredMixin, View):
    """ View for accessing remittances of a pledge """

    def post(self, request, *args, **kwargs):
        """ Update pledge information for a case """
        try:
            user = request.user
            case = CaseDetail.objects.get(pk=kwargs['case_id'])
            case_pledge = CasePledge.objects.get(pk=kwargs['pledge_id'])

            case_pledge.remitted = request.POST['remitted']
            case_pledge.save()

            for proof_file in request.FILES.values():
                RemittanceProof.objects.create(
                    attachment=proof_file,
                    pledge=case_pledge
                )

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Information saved successfully'
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    'status': 'failure',
                    'message': 'Something went wrong!',
                },
                status=500
            )
