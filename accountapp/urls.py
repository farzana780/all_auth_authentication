from django.urls import path, include
from accountapp import views
from accountapp.views import ChangePasswordView, LogoutView, EmailConfirmation



urlpatterns = [
    path('test/', views.test, name='test'),
    path('login/', views.login),
    path('refresh_login/', views.refresh_login),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view()),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('sendconfirmationemail/', EmailConfirmation.as_view(), name='send-email-confirmation')

]
