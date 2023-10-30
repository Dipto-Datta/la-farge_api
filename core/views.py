from datetime import timedelta,datetime
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView

from django.contrib.auth.models import Group, Permission


#import custom permission classes
from .permissions import default_user,admin_user
# imort model
from .models import User

# import serializers
from .serializers import UserRegisterSerializer,UserDetailSerializer,PasswordChangeSerializer,UserLoginSerializer,GroupSerializer,PermissionSerializer



# todo ----- handle error using try cathch 

@api_view(['POST'])
def registration(request):
    # check if both passwords are same
    # if not same -> returns 403

    if request.data['password'] != request.data['confirm_password']:
        return Response({
        'message':"Both password should match"
    },status=status.HTTP_403_FORBIDDEN)

    
    # checks if an user with the given email exists
    # if exists -> returns 403

    user = User.objects.filter(email=request.data['email'])
    #print(user)
    if user:
        
        return Response({
        'message':"An user with this email already exists"
    },status=status.HTTP_403_FORBIDDEN)
    
    # serialize request data
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(email=request.data['email'])

        # sets hashed password
        user.set_password(request.data['password'])
        user.save()

        # generates refresh token
        refreshToken = RefreshToken.for_user(user)
        accessToken = refreshToken.access_token
        decodeJTW = jwt.decode(str(accessToken), settings.SECRET_KEY, algorithms=["HS256"])

        # Todo: add your payload here!!
        decodeJTW['email'] = user.email
        decodeJTW['date'] = datetime.now().timestamp()
        # decodeJTW['id'] = user.id
        #encode
        encoded = jwt.encode(decodeJTW, settings.SECRET_KEY, algorithm="HS256")
        return Response({
        'status': True,
        'refresh': str(refreshToken),
        'access': str(encoded),
        
    })
    return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    # token, created = Token.objects.get_or_create(user=user)
    serializer = UserLoginSerializer(user)
    # return Response({'token': token.key, 'user': serializer.data})
    refreshToken = RefreshToken.for_user(user)
    accessToken = refreshToken.access_token

    decodeJTW = jwt.decode(str(accessToken), settings.SECRET_KEY, algorithms=["HS256"]);
    # print(decodeJTW)

    # Todo: add your payload here!!
    decodeJTW['email'] = user.email
    decodeJTW['date'] = datetime.now().timestamp()
    # decodeJTW['id'] = user.id


    #encode
    encoded = jwt.encode(decodeJTW, settings.SECRET_KEY, algorithm="HS256")

    return Response({
        'status': True,
        'refresh': str(refreshToken),
        'access': str(encoded),
        'user':serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_super_user(request):

    if request.data['password'] != request.data['confirm_password']:
        return Response({
        'message':"Both password should match"
    },status=status.HTTP_403_FORBIDDEN)

    
    # checks if an user with the given email exists
    # if exists -> returns 403

    user = User.objects.filter(email=request.data['email'])
    #print(user)
    if user:
        
        return Response({
        'message':"An user with this email already exists"
    },status=status.HTTP_403_FORBIDDEN)
    
    # serialize request data
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        user = User.objects.create_superuser('admin',data.get('email'),data.get('password'))
        print(user,'-> create_super_user function')
        user.save()
        return Response({
        'status': True
        #'refresh': str(refreshToken),
        #'access': str(encoded),
    })
    return Response(serializer.errors, status=status.HTTP_200_OK)



class user_list_view(viewsets.ModelViewSet):
    permission_classes = [admin_user]
    queryset = User.objects.all()#.exclude(userType="Super Admin")
    pagination_class = None
    serializer_class = UserDetailSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_fields = [ 'name','email','created_at','updated_at']



# class PasswordResetView(GenericAPIView):
#     """
#     Calls Django Auth PasswordResetForm save method.

#     Accepts the following POST parameters: email
#     Returns the success/fail message.
#     """
#     serializer_class = api_settings.PASSWORD_RESET_SERIALIZER
#     permission_classes = (AllowAny,)
#     throttle_scope = 'dj_rest_auth'

#     def post(self, request, *args, **kwargs):
#         # Create a serializer with request.data
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         serializer.save()
#         # Return the success message with OK HTTP status
#         return Response(
#             {'detail': _('Password reset e-mail has been sent.')},
#             status=status.HTTP_200_OK,
#         )


# class PasswordResetConfirmView(GenericAPIView):
#     """
#     Password reset e-mail link is confirmed, therefore
#     this resets the user's password.

#     Accepts the following POST parameters: token, uid,
#         new_password1, new_password2
#     Returns the success/fail message.
#     """
#     serializer_class = api_settings.PASSWORD_RESET_CONFIRM_SERIALIZER
#     permission_classes = (AllowAny,)
#     throttle_scope = 'dj_rest_auth'

#     @sensitive_post_parameters_m
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {'detail': _('Password has been reset with the new password.')},
#         )



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):

    serializer = PasswordChangeSerializer(data=request.data)
    if serializer.is_valid():
        
        validatedData = serializer.validated_data

        # if new_password and confirm_password doesnot matches returns 406
        if validatedData.get('new_password') != validatedData.get('confirm_password'):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE) 
        

        old_password = validatedData.get('old_password')

        # retriving accesstoken
        access_token=request.headers['Authorization'].split(' ')[1]
        # decoding payload
        decodeJTW = jwt.decode(str(access_token), settings.SECRET_KEY, algorithms=["HS256"])
        # search user using decoded payload user id, if user not found return error 404 
        logged_in_user = get_object_or_404(User, id=decodeJTW['user_id'])

        # compare old_password with db's hashed password
        # if matches - proceed: else return error 406
        if logged_in_user.check_password(old_password):
            logged_in_user.set_password(validatedData.get('new_password'))
            logged_in_user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    
    try:
        # todo: save current accessToken in DB and set delete after exp time  
        refreshToken = RefreshToken(request.data['refresh'])
        refreshToken.blacklist()
        response = Response(
        {'detail':('Successfully logged out.')},
        status=status.HTTP_200_OK,)
        return response
    except KeyError:
        response = Response(
        {'detail':('Refresh token was not included in request data.')},
        status=status.HTTP_401_UNAUTHORIZED,)
      
        return response




# this endpoint was created for verify JWT- Now using TokenVerification | NOT BEING USED ANYMORE
# todo : Improve or remove
@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def token_validation(request):
    response = Response(
        {'detail':('Verifieed')},
        status=status.HTTP_200_OK,)
    return response


class group_list_view(viewsets.ModelViewSet):
    # permission_classes([IsAuthenticated])
    permission_classes = [admin_user]
    queryset = Group.objects.all()#.exclude(userType="Super Admin")
    pagination_class = None
    serializer_class = GroupSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    # filterset_fields = [ 'name','email','created_at','updated_at']

class permission_list_view(viewsets.ModelViewSet):
    # permission_classes([IsAuthenticated])
    permission_classes = [admin_user]
    queryset = Permission.objects.all()#.exclude(userType="Super Admin")
    pagination_class = None
    serializer_class = PermissionSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    # filterset_fields = [ 'name','email','created_at','updated_at']

# Assuming you have an application with an app_label foo and a model named Bar, to test for basic permissions you should use:

# add: user.has_perm('foo.add_bar')
# change: user.has_perm('foo.change_bar')
# delete: user.has_perm('foo.delete_bar')
# view: user.has_perm('foo.view_bar')
