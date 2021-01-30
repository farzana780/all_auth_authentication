from django.contrib.auth import logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django_rest_passwordreset.models import ResetPasswordToken
from oauth2_provider.admin import AccessToken, Application
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from accountapp.models import CustomUser
from accountapp.serializers import UserSerializer, ChangePasswordSerializer, EmailChangeSerializer
from django.http import JsonResponse
from rest_framework import generics, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
import requests


@csrf_exempt
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def User_data(request):
    user_id = request.user.pk

    token = AccessToken.objects.get(token=request.data['token'])
    users = CustomUser.objects.get(id=token.user_id)
    user_serialiser = UserSerializer(users, many=False)
    return JsonResponse({'user': user_serialiser.data})


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user = authenticate(email=request.data['username'], password=request.data['password'])
    if user:
        r = requests.post(
            'http://0.0.0.0:8000/o/token/',
            data={
                'grant_type': 'password',
                'username': request.data['username'],
                'password': request.data['password'],
                'client_id': request.data['client_id'],
                'client_secret': request.data['client_secret'],
            },
        )
        return Response(r.json())
    else:
        message = {
            'status': 'wrong username & password'
        }
        return JsonResponse(message)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_login(request):

    r = requests.post('http://0.0.0.0:8000/o/token/',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id':  request.data['client_id'],
            'client_secret': request.data['client_secret'],
        },
    )
    return Response(r.json())


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self, request, format=None):
        token = AccessToken.objects.get(token=request.data['token'])
        user_name = Application.objects.get(client_id=token.application.client_id)
        Client_id = user_name.client_id
        Client_secret = user_name.client_secret
        r = requests.post(
            'http://0.0.0.0:8000/o/revoke_token/',
            data={
                'token': request.data['token'],
                 'client_id':  Client_id,
                 'client_secret': Client_secret,
            },
        )
        logout(request)
        response = Response({"detail":("Successfully logged out.")},
                            status=status.HTTP_200_OK)
        return response


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    reset_token_user = ResetPasswordToken.objects.get(user_id=reset_password_token.user_id)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Forget password"),

        # message:
        "Key {token}".format(token=reset_token_user.key),


        # from:
        "admin@gmail.com",
        # to:
        [reset_password_token.user.email]
    )


from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress



class EmailConfirmation(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email_address = EmailAddress.objects.get(email=request.data['email'])
        if email_address.verified:
            return Response({'message': 'Email already verified'}, status=status.HTTP_201_CREATED)

        send_email_confirmation(request, request.user)
        return Response({'message': 'Email confirmation resent'}, status=status.HTTP_201_CREATED)



class UpdateEmail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = EmailAddress.objects.all()
        serializer = EmailChangeSerializer(user, many=True)
        return Response(serializer.data)

    #first token theke user get korben
    #than email update korben
    #than ager email delete kore diben
    #if need multiple function call korben
    #user id ei gulo token theke get korben
    #wait ami akta method dicchi

    #request.user.pk
    #bujhte parsen??????
    #vaia user_id token theke get hoy but user_id ar email address er ei table er id different
    #but relation same
    #bujhte parsen. ji vaia
    #aj kintu sesh korben . ji


    def patch(self, request, format=None):

        user_id = request.user.pk #okay

        #ekhane update delete sob korben by using token

        #i hope you are understand . ji vaia bujhte peresi ar problem hole janabo
        #kaj ajke sesh korben
        #best of luck

        #by default verified thakar kotha na????ji vaia eta thik korte hobe
        #hmm koren


        #Key 68247  5ta keno???? 6 ta howar kotha na???? try koren keno hocche na .ji

        token = AccessToken.objects.get(token=request.data['token'])
        user_object = CustomUser.objects.get(id=token.user_id)
        user_email = EmailAddress.objects.get(user=user_object.id)
        user_email.verified = False
        user_object.email = request.data.get("email", user_object.email)
        user_object.save()
        serializer = EmailChangeSerializer(user_email, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        request.user = user_object

        send_email_confirmation(request, request.user)
        return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)


'''
hoyni kicchu????
*1. email change korar somoy ami just token & new email dibo. baki kaj web app kore felbe. 
*2. just 1 ta api call hobe
*3. sign up thik koren 
'''
