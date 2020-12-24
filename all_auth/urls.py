from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from allauth.account.views import confirm_email


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('accountapp.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'rest-auth/', include('rest_auth.urls')),
    url(r'rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'accounts/', include('allauth.urls')),
    url(r'accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
]
