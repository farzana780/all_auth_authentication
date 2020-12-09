from django.conf.urls import url
from django.urls import path, include
from accountapp import views


urlpatterns = [
    path('test/', views.test, name='test' ),
    # url(r'sign_up/', views.SignUp.as_view(), name="sign_up"),
    # path('register/', views.register),
    path('login/', views.login),

]

