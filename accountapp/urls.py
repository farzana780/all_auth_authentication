from django.urls import path, include
from accountapp import views
from accountapp.views import ChangePasswordView, LogoutView, EmailConfirmation

urlpatterns = [
    path('test/', views.test, name='test' ),
    # url(r'sign_up/', views.SignUp.as_view(), name="sign_up"),
    # path('register/', views.register),
    path('login/', views.login),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    # path('logout/', LogoutApi.as_view({'post': 'logout'})),
    path('logout/', LogoutView.as_view()),
    # path('logout/', views.logout_user),
    # path('revoke_token/', views.revoke_token),
    # path('hello/', views.hello_world, name='hello'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('sendconfirmationemail/', EmailConfirmation.as_view(), name='send-email-confirmation')

]

'''
forgot password
*resent email verification
password change
logout
'''

