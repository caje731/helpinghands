from django.template import Library, Node, TemplateSyntaxError, Variable

from donations.models import CasePledge
register = Library()

@register.filter
def pledged_by(case, user):
    """ Get amount pledged by a user for a case """
    print 'asdfas'
    try:
        pledge = CasePledge.objects.get(user=user, case=case)
        return pledge.amount
    except CasePledge.DoesNotExist:
        return 0