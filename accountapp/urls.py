from django.conf.urls import url
from django.urls import path, include
from accountapp import views
from accountapp.views import ChangePasswordView, LogoutView, EmailConfirmation, UpdateEmail

urlpatterns = [
    path('user_data/', views.User_data, name='user_data'),
    path('login/', views.login),
    path('refresh_login/', views.refresh_login),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('change_email/<int:pk>/', UpdateEmail.as_view(), name='change-email'),
    path('change_email/', UpdateEmail.as_view()),

    path('logout/', LogoutView.as_view()),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('resendconfirmationemail/', EmailConfirmation.as_view(), name='send-email-confirmation')

]
