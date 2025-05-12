from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from . serializer import (
    UserTypeSerializer,
    UserLoginBaseSerialize, 
    OtpBaseSerializer, 
    UserRegistrationBaseSerialize, 
    UserSerialize, 
    UserEditProfileBaseSerializer, 
    ProfileModalSerializer,
    UserTypeModelSerializer,
    UserUpdateSerializer,
    DeleteUserSerializer,
    UserPasswordChangeSerializer,
    UserCountSerializer,
    profileSerializer
)
from system_management.models import Profile, User, Otp, Usertype,Attempts
from .generate_otp import generate_numeric_otp
import json
from django.utils import timezone
from rest_framework.authtoken.models import Token
from .send_sms import send_otp
from .send_email import email_send
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from .base_url_mod import base_url
from system_management import constants
from django.db.models import Q

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        serializer = UserLoginBaseSerialize(data=body)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']   
            user = authenticate(username=username, password=password)
           
            if user and user.is_active:
                if not user.check_password(password):
                    user = None
            if user:
                user_id = user.id
                role_type = user.user_type.type
                fullname = user.first_name + ' ' + user.last_name
                token,_ = Token.objects.get_or_create(user_id=user_id)
                otp = generate_numeric_otp(4)
                Otp.objects.update_or_create(
                user_id=user.id,
                defaults= {
                    'otp':otp
                }
                )
                data = json.dumps({
                    'token': token.key,
                    'user_id': user_id,
                    'user_type': role_type,
                    'fullname': fullname,
                    'status': 'success',
                    'message': 'Login Successfully'
                })
                return Response(data, status=status.HTTP_200_OK)
            
            else:
                data = json.dumps({
                    'status': 'error',
                    'message': 'Invalid login'
                })
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = json.dumps({
                'status': 'error',
                'message': serializer.errors
            })
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['POST','GET'])
def verify_otp(request):
    if request.method == 'GET': 
        user= request.user
        try:
            otp_obj = Otp.objects.get(user_id = user.id)

        except Otp.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message':'OTP object does not exist'
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cell_number = Profile.objects.get(user_id=user.id).phone_number
        
        except Profile.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message':'Profile object does not exist'
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
       
        if otp_obj:
            context = {
                'otp':otp_obj.otp,
                'first_name':user.first_name,
                'last_name':user.last_name,
               
            }
            
            send_otp(user.first_name,user.last_name,otp_obj.otp,cell_number)
            html_tpl_path = 'emails/otp_email.html'
            email_send(context, user.email,html_tpl_path)
            data = json.dumps({
                'status': 'success',
                'otp':otp_obj.otp,
            })
            return Response(data=data, status=status.HTTP_200_OK)
        
        else:
            data = json.dumps({'status':'error','message': 'runtime error'})
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)    
        
    if request.method == 'POST':
        user = request.user
        body = json.loads(request.body)
        serializer = OtpBaseSerializer(data=body)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']  
            try:            
                otp_obj = Otp.objects.get(otp=otp, user_id=user.id)
                
                if otp_obj:

                    Response_data = {
                        'is_first_login':user.is_first_login
                    }

                    data = json.dumps({
                        'status': 'success',
                        'message':'OTP verified successful',
                        'data': Response_data
                    })
                    otp = generate_numeric_otp(4)
                    otp_obj.otp = otp
                    otp_obj.save()
                    return Response(data=data, status=status.HTTP_200_OK)
            except Otp.DoesNotExist:
                try:
                    attempt_obj = Attempts.objects.filter(user_id=user.id, type_id__type=constants.OTP_TYPE).first()
                    if not attempt_obj.last_update:
                        attempt_obj.last_update = timezone.now() - timezone.timedelta(hours=5)
                    remaining_time = timezone.now() - attempt_obj.last_update
                    if attempt_obj.no_attempts > 0 and remaining_time >= timezone.timedelta(hours=5):
                        attempt_obj.no_attempts = 0
                        attempt_obj.last_update = timezone.now()
                    attempt_obj.no_attempts += 1
                    attempt_obj.save()
                    context = {
                        'attempts': attempt_obj.no_attempts,
                        'time_left': remaining_time.total_seconds(),  # Convert to seconds for JSON serialization
                    }
                    data = json.dumps({'status':'error','message': 'Invalid OTP, you are left with','time_left':context,})
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                except Attempts.DoesNotExist:
                    data = json.dumps({'status':'error','message':'Attempts doesnt exist'})

        else:
            data = json.dumps({
                    'status': 'error',
                    'message': serializer.errors
                })

            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    
    if request.method == 'POST':
        
        try:
            token= Token.objects.get(user_id=request.user)
            token.delete()
            response_data = json.dumps({
                'status': 'success', 
                 'message': 'Logout Successfully'
            })
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Token.DoesNotExist:
            detail = 'Token does not exist'
            response_data = json.dumps({'status': 'error', 'message': detail})
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def profile_api(request):
    if request.method == 'GET':
        profile = Profile.objects.filter(user_id=request.user.id)

        if profile.exists():
            serializer = ProfileModalSerializer(instance=profile,many = True)
            data = json.dumps ({
                'status': 'success',
                'profile': serializer.data,
                'message': 'Profile fetched successfully'
                
            })

            return Response(data=data, status=status.HTTP_200_OK)
        
        else:
            data = json.dumps ({
                'status': 'error',
                'message': 'Profile does not exist'
            })
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        
        body =json.loads(request.body)


        serializer = UserEditProfileBaseSerializer(data=body) 

        if serializer.is_valid():
            
            email = serializer.validated_data['email']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            phone_number = serializer.validated_data['phone_number']
            gender = serializer.validated_data['gender']
            identity_number = serializer.validated_data['identity_number']
            passport_number = serializer.validated_data['passport_number']
            date_of_birth = serializer.validated_data['date_of_birth']
            ethnicity = serializer.validated_data['ethnicity']
            address = serializer.validated_data['address']
        
            User.objects.filter(id=request.user.id).update(
                email=email,
                first_name=first_name,
                last_name=last_name ,

            )
            if passport_number == None: 
                passport_number = ""

            if identity_number == None:
                identity_number = ""

            Profile.objects.filter(user_id=request.user.id).update(
                phone_number=phone_number,
                gender=gender,
                identity_number=identity_number,
                passport_number=passport_number,
                date_of_birth=date_of_birth,
                ethnicity=ethnicity,
                address=address

            )

            data = json.dumps({
                'status': 'success',
                'message': 'Profile updated successfully'
            })
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            
            data = json.dumps({
                'status': 'error',
                'message': str(serializer.errors)
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data =json.dumps({
                'status': 'error',
                'message': serializer.errors
            })
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dashboard_api(request):
    if request.method == 'GET':
        user_count = User.objects.all().count()
        if user_count:
            serializer = UserCountSerializer(data = {'user_count': user_count})
            if serializer.is_valid():
                user_count = serializer.validated_data['user_count']
                data = json.dumps({

                    'status': 'success',
                    'message': 'User count',
                    'data': user_count,
                })
                return Response(data=data, status=status.HTTP_200_OK) 
            else:
                data = json.dumps({
                    'status': 'error','message':'error serializing data'
                })
                    

        else:
            data = json.dumps({'status': 'error', 'message': 'user objetct not found'})
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)   



@api_view(['GET'])
def users_api_get(request):
    user = request.user

    if request.method == 'GET':
        users = User.objects.filter(
            ~Q(user_type__type=constants.ADMIN) &
            ~Q(id=user.id)
        )
        user_types = Usertype.objects.all()
        user_profile = Profile.objects.filter(user_id=user.id)

        prof_serializer = profileSerializer(instance=user_profile, many=True)
        serializer = UserSerialize(instance=users, many=True)
        type_serializer = UserTypeModelSerializer(instance=user_types, many=True)
        
        data = json.dumps({
            'status': 'success',
            'message': 'User details',
            'data': serializer.data,
            'user_types': type_serializer.data,
            'user_profile': prof_serializer.data,
            
        })

        return Response(data=data, status=status.HTTP_200_OK)


        
@api_view(['POST'])
def users_api_post(request):
    if request.method == "POST":
        body = json.loads(request.body)
        serializer = UserRegistrationBaseSerialize(data=body)

        if serializer.is_valid():
           first_name = serializer.validated_data.get('first_name')
           last_name = serializer.validated_data.get('last_name')
           email = serializer.validated_data.get('email')
           password = serializer.validated_data.get('password')
           user_type = serializer.validated_data.get('user_type')
           phone_number = serializer.validated_data.get('phone_number')

        else:
            data = json.dumps({
                'status': "error",
                'message': serializer.errors
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST) 
           
        user_type_obj = Usertype.objects.get(id=user_type).id

        user = User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
            user_type_id = user_type_obj, 
        )

        Profile.objects.create(
                user_id = user.id,
                phone_number = phone_number,
            )
        if user:
            url = f'{base_url(request)}'
            context = {
                    'user_password': password,
                    'user_first_name': user.first_name,
                    'user_email': user.email,
                    'login_url':url,
                }
            
            html_tpl_path = 'emails/email_welcome.html'
            email_send(context, user.email,html_tpl_path)

            data = json.dumps({
                'status':   'success',
                'message': 'User registered successfully'
            })
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = json.dumps({
                'status': 'error',
                'message': 'User registration failed',
                'data': serializer.errors
            })

    else:

        data = json.dumps({
            'status': 'error',
            'message':'Invalid method used.'
        })
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
   
    
@api_view(['GET'])
def resend_otp_api(request):
    if request.method == 'GET':
        reset_url = f'{base_url(request)}{reverse("update_password_api")}'
        user= request.user
        try:
            otp_obj = Otp.objects.get(user_id = user.id)
        except Otp.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message':'OTP object does not exist'
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        try:
            cell_number = Profile.objects.get(user_id=user.id).phone_number
        
        except Profile.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message':'Profile object does not exist'
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
       
        try:
            user_obj = User.object.get(pk=user.id)
        except User.DoesNotExist:
            data = json.dumps({
                'status': 'error',
                'message':'User object does not exist'
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
       
        if otp_obj:
            context = {
                'otp':otp_obj.otp,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'reset_url':reset_url,
            }
            send_otp(user.first_name,user.last_name,otp_obj.otp,cell_number)
            html_tpl_path = 'emails/otp_email.html'
            email_send(context,user.email,html_tpl_path)
            data = json.dumps({
                'status': 'success',
                'message':'OTP verified successful'
            })
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            data = json.dumps({'status':'error','message': 'runtime error'})
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)    

@api_view(['POST'])
def delete_user_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = DeleteUserSerializer(data=data)
        
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
         
            
            try:
                user = User.objects.get(pk=user_id)
        
            except User.DoesNotExist:
                data = json.dumps({
                    'status': 'error',
                    'message': f'User with ID {user_id} does not exist'
                })
                return Response(data, status=404)

            user.delete()
            data = json.dumps({
                'status': 'success',
                'message': 'User deleted successfully'
            })
            return Response(data, status=200)
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def update_user_api(request):

    if request.method == 'POST':
        body = json.loads(request.body)
        serializer = UserUpdateSerializer(data=body)

        if serializer.is_valid():
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            phone_number = serializer.validated_data['phone_number']
            user_id = serializer.validated_data['user_id']

            User.objects.filter(id=user_id).update(
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            Profile.objects.filter(user_id=user_id).update(
                phone_number=phone_number,
                
            )

            data = json.dumps({
                'status': 'success',
                'message': 'User updated successfully'
            })

            return Response(data=data, status=status.HTTP_200_OK)
        
        else:
            data = json.dumps({
                'status': 'error',
                'message': serializer.errors,
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_password_api(request):
        user = request.user
        if request.method == 'POST':
            body = json.loads(request.body)
            serializer = UserPasswordChangeSerializer(data=body)
            if serializer.is_valid():
                new_password = serializer.validated_data['password']
                if user:
                    hashed_password = make_password(new_password)
                    user.password = hashed_password
                    user.is_first_login = False
                    user.save()
                    data = json.dumps({
                        'status': 'success',
                        'message': 'Well done!, Welcome to the Deep-end'
                    })
                    return Response(data=data, status=status.HTTP_200_OK)
                else:
                    data = json.dumps({
                        'status': 'error',
                        'message': 'Old password is incorrect'
                    })
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            else:
                data = json.dumps({
                    'status': 'error',
                    'message': 'Password not updated'
                })
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST) 