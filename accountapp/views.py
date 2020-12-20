from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.admin import AccessToken, Application, AccessTokenAdmin
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from accountapp.models import CustomUser
from accountapp.serializers import UserSerializer, ChangePasswordSerializer
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import requests


@csrf_exempt
@authentication_classes([OAuth2Authentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def test(request):
    token = AccessToken.objects.get(token=request.data['token'])
    users = CustomUser.objects.get(id=token.user_id)
    user_serialiser = UserSerializer(users, many=False)
    # json_data = JSONRenderer().render(user_serialiser.data)
    return JsonResponse({'user': user_serialiser.data})


# from rest_framework import generics
#
#
# class SignUp(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CreateUserSerializer
#     permission_classes = (IsAuthenticated,)
#
#


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     '''
#     Registers user to the server. Input should be in the format:
#     {"username": "username", "password": "1234abcd"}
#     '''
#     # Put the data from the request into the serializer
#     serializer = CreateUserSerializer(data=request.data)
#     # Validate the data
#     if serializer.is_valid():
#         # If it is valid, save the data (creates a user).
#         serializer.save()
#         # Then we get a token for the created user.
#         # This could be done differentley
#
#         return Response('Successfully Registered')
#     return Response(serializer.errors)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    '''
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    '''
    r = requests.post(
    'http://127.0.0.1:8000/o/token/',
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
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

# @csrf_exempt
# def revoke_token(request):
#     r = requests.post(
#         'http://127.0.0.1:8000/o/revoke_token/',
#         data={
#             'token': '64b0BIfvzasq8hIzznWZWtM9unvQe7',
#             'client_id': 'zk5yn8JDDjkGkAeAElrNgTE5je3EXbtUc697hZCt',
#             'client_secret': 't1PC3bbBzv9LIJRmHGrGAn3nmkQhzBznhTwmULC2DyEdKGoI5jBKziyQhOIJSpCGxzrbI147GpGnzS7SAXmfIBKbn4igrzvZDpdL0J8tMznJ85J8dqOzGnNHgytUDORS',
#         },
#     )
#     return r
#

# just make a request here
# POST /o/revoke_token/ HTTP/1.1 Content-Type: application/x-www-form-urlencoded token=XXXX&client_id=XXXX&client_secret=XXXX

# @csrf_exempt
# def logout_user(self, request):
#     r = requests.post(
#         'http://127.0.0.1:8000/o/revoke_token/',
#         data={
#             'token': '64b0BIfvzasq8hIzznWZWtM9unvQe7',
#             'client_id': 'zk5yn8JDDjkGkAeAElrNgTE5je3EXbtUc697hZCt',
#             'client_secret': 't1PC3bbBzv9LIJRmHGrGAn3nmkQhzBznhTwmULC2DyEdKGoI5jBKziyQhOIJSpCGxzrbI147GpGnzS7SAXmfIBKbn4igrzvZDpdL0J8tMznJ85J8dqOzGnNHgytUDORS',
#         },
#     )
#     # if succeed
#     logout(request)
#     response = {
#         'status': 'success',
#         'code': status.HTTP_200_OK,
#         'message': 'Logged Out successfully',
#     }
#     return Response(response)

#
# def logout(self, request):
#     self.logout(request)
#     return Response({"success": ("Successfully logged out.")},
#                     status=status.HTTP_200_OK)
#
#


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
            'http://127.0.0.1:8000/o/revoke_token/',
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

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Forget password"),
        # message:
        email_plaintext_message,
        # from:
        "admin@gmail.com",
        # to:
        [reset_password_token.user.email]
    )


from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailAddress
# request a new confirmation email
class EmailConfirmation(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = CustomUser.objects.get(email=request.data['email'])
        email_address = EmailAddress.objects.get(email=email)
        if email_address.verified:
            return Response({'message': 'Email already verified'}, status=status.HTTP_201_CREATED)

        send_email_confirmation(request, request.user)
        return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)
