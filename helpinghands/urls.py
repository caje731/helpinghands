"""helpinghands URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from donations import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    
    # URLs for the navigation bar
    url(r'^about/$', TemplateView.as_view(template_name='donations/nav_bar/about_us.html'), name='about'),
    url(r'^faq/$', TemplateView.as_view(template_name='donations/nav_bar/FAQ.html'), name='faq'),
    url(r'^people/$', TemplateView.as_view(template_name='donations/nav_bar/people.html'), name='people'),
    url(r'^tou/$', TemplateView.as_view(template_name='donations/nav_bar/TOU.html'), name='tou'),
    url(r'^privacy/$', TemplateView.as_view(template_name='donations/nav_bar/privacy_policy.html'), name='privacy'),
    url(r'^external/$', TemplateView.as_view(template_name='donations/nav_bar/helpful_links.html'), name='external'),
    url(r'^donor/signup/$', views.DonorSignupView.as_view(), name='donor_signup'),
    
    # Use the default auth views which give the following urls:
    # ^login/$ [name='login']
    # ^logout/$ [name='logout']
    # ^password_change/$ [name='password_change']
    # ^password_change/done/$ [name='password_change_done']
    # ^password_reset/$ [name='password_reset']
    # ^password_reset/done/$ [name='password_reset_done']
    # ^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
    # ^reset/done/$ [name='password_reset_complete']
    url('^accounts/logout/', views.logout_view, name="logout"),
    url('^accounts/', include('django.contrib.auth.urls')),
    url('^accounts/profile/', views.ProfileView.as_view(), name="profile"),
]
