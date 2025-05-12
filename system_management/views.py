import json
from .password_gen import generate_password
from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import render
import requests
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from .models import User

def base_url(request):
    protocol = request.scheme
    host = request.get_host()
    host_url = f'{protocol}://{host}'
    return host_url


def keep_session_alive(request):
    request.session.set_expiry(1800)
    return JsonResponse(data=json.dumps({'status': 'success'}))


def password_update(request): 
    if request.method == 'GET':
        return render(request,'password_reset_form.html')
    
    if request.method == 'POST':
            token =request.session.get("token")
            url = f'{base_url(request)}{reverse("update_password_api")}'
            new_password = request.POST.get('password')
            header = {
                'content-type':'application/json',
                'Authorization':f'Token {token}'}
            payload = json.dumps({
                'password':new_password,
            })
            response = requests.request('POST', url=url, data=payload, headers=header)
            response_data = json.loads(response.json())
            token = response_data.get('token') 
            return JsonResponse(data=response_data, safe=False)


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        url = f'{base_url(request)}{reverse("login")}'
        payload = json.dumps({
            "username": username,
            "password": password,
        })
        headers = {
            'content-type': 'application/json',
        }
        response = requests.request('POST', url, data=payload, headers=headers)
        response_data = json.loads(response.json())
        token = response_data.get('token')    
        if token:
            request.session['token'] = token  
            user_id = response_data['user_id']  
            fullname = response_data['fullname']
            role_type = response_data['user_type']
            fullname = response_data['fullname']
            request.session['user_id'] = user_id
            request.session['fullname'] = fullname
            request.session['user_type'] = role_type
            
        return JsonResponse(data=response_data, safe=False)
    else:
        data = json.dumps({
            'status': 'error',
            'message': 'Wrong methods used',
        })
        return JsonResponse(data=data, status=400)


def otp_views(request):
    token = request.session.get('token')
    url = f'{base_url(request)}{reverse("otp_verify")}'
    headers = {
            'content-type': 'application/json',
            'Authorization':f'Token {token}'
    }
    if request.method == 'GET':
        response = requests.request("GET", url, headers=headers)
        return render(request, 'otp.html')
            
    if request.method == 'POST':
        token = request.session.get('token')
        entered_otp = request.POST.get('otp')
        payload = json.dumps({
            'otp': entered_otp,
        })
        url = f'{base_url(request)}{reverse("otp_verify")}'
        headers = {
            'content-type': 'application/json',
            'Authorization':f'Token {token}'
        }
        if entered_otp:
            response = requests.request("POST", url, data=payload, headers=headers)
            response_data = json.loads(response.json())
            if response_data.get("status") == "success":
                request.session['is_verified'] = True
                if response_data['data']['is_first_login']:
                    redirect_url = f"{base_url(request)}{reverse('password_update')}"
                else:
                    redirect_url = f"{base_url(request)}{reverse('app_dashboard')}"
                    response_data = {
                        'status':'success',
                        'redirect_url':redirect_url,
                        'message':'OTP verified successfully'
                    }
                return JsonResponse(response_data,status=200)
            else:    
                return JsonResponse(response_data,status=400)


def app_dashboard(request):
    token = request.session.get('token')
    url = f'{base_url(request)}{reverse("dashboard_api")}'
    headers = {
        'content-type': 'application/json',
        'Authorization':f'Token {token}'
    }
    if request.method == "GET":
        payload = json.dumps({})
        response = requests.request(method="GET", url=url , headers=headers, data=payload)
        response_data = json.loads(response.json())
        context ={
            'user_number':response_data['data'],
        }
        return render(request, 'dashboard.html', context)


def users_view(request):
    if request.method == 'GET': 
        token = request.session.get('token') 
        user_id = request.session.get('user_id')

        if token is None:
            return redirect('login_view')
        
        url = f'{base_url(request)}{reverse("users_api_get")}'
        payload = json.dumps({})
        headers = {
            'content-type': 'application/json',
            'Authorization':f'Token {token}'
        }
        response = requests.request(method="GET", url=url , headers=headers, data=payload)  
    
        if response.status_code == 200:
            users = json.loads(response.content)
            users = json.loads(users)
        
            context = { 
                'users': users['data'],
                'user_types': users['user_types'],
                'user_profile': users['user_profile'],         
                }
        
        return render(request, 'users.html', context)
   

    if request.method == 'POST':
        token = request.session.get('token') 

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = int(request.POST.get('user_type'))
        phone_number = request.POST.get('phone_number')
        
        url = f'{base_url(request)}{reverse("users_api_post")}'
        password = generate_password(30,True)

        payload = json.dumps({
            "first_name":first_name,
            "last_name":last_name,
            "email":email,
            "password":password,
            "confirm_password":confirm_password,
            "user_type": user_type,
            "phone_number" : phone_number,
        })

        headers = {
            'content-type': 'application/json',
            'Authorization':f'Token {token}'
        }

        response = requests.request(method="POST", url=url, headers=headers, data=payload)

        if response.status_code == 200:
            response_data = json.loads(response.json())
            return JsonResponse({'status':'success'}, status=200)
        else :
            return JsonResponse({'status':'error', 'message': 'Failed to create user'}, status=400)
        



def password_reset_view(request):
    token = request.session.get('token') 
    payload = json.dumps({})
    url = f'{base_url(request)}{reverse("password_reset_form")}'
    headers = {
        'content-type': 'application/json',
        'Authorization':f'Token {token}'
    }
    if request.method == "GET":
        response = requests.request("GET", url, headers=headers, data=payload)
        return render(request, 'password_reset_form.html')

    
def document_view(request):
    
    return render(request, 'document.html')


def profile_view(request):

    if request.method == 'GET':
        token = request.session.get('token')
        url = f'{base_url(request)}{reverse("profile_api")}'
        payload = json.dumps({})
        headers = {
            'content-type': 'application/json',
            'Authorization':f'Token {token}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response_data = json.loads(response.json())
        
        profile = response_data.get('profile')
        context = {
            'profile':profile
            }
        return render(request, 'profile.html', context)

    if request.method == 'POST':
        token = request.session.get('token')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        identity_number = request.POST.get('identity_number')
        passport_number = request.POST.get('passport_number')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        ethnicity = request.POST.get('ethnicity')


        url = f'{base_url(request)}{reverse("profile_api")}'

        payload = json.dumps({
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "gender": gender,
            "identity_number":identity_number,
            "passport_number":passport_number,
            "date_of_birth":date_of_birth,
            "address":address,
            "ethnicity":ethnicity
        })
        
        headers = {
            'content-type': 'application/json',
            'Authorization':f'Token {token}'
        }
       
        response = requests.request("POST", url=url, data=payload, headers=headers)
        response_data = json.loads(response.json())

        
        return JsonResponse(response_data, status=200)


def graphs_view(request):
    return render(request, 'graphs.html')


def logout_view(request):
    token = request.session.get('token')
    session_key = request.session.session_key
    try:
        session_obj = Session.objects.get(session_key=session_key)
        session_obj.delete()
        url = f"{base_url(request)}{reverse('logout')}"
        payload = json.dumps({})
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Token {token}'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response_data = json.loads(response.json())
        return JsonResponse(data=response_data, safe=True)
    
    except Session.DoesNotExist:
        
        error_data = {'error': 'Logout failed'}
    return JsonResponse(error_data, status=400)


def resend_otp(request):
    url=f'{base_url(request)}{reverse("resend_otp_api")}'
    token = request.session.get('token')

    payload = json.dumps({})
    headers = {
            'content-type': 'application/json',
            'Authorization':f'Token {token}'
    }
    if request.method == 'GET':
        response = requests.request("GET", url, headers=headers,data=payload)
        response_data = json.loads(response.json())
        return JsonResponse(response_data, status=200)


def user_update_view(request):

    token = request.session.get('token')

    if request.method == 'POST':

        url = f'{base_url(request)}{reverse("update_user_api")}'
        
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        payload = json.dumps({ 
            "user_id": user_id,
            "first_name": first_name,
            "last_name": last_name, 
            "email": email, 
            "phone_number": phone_number,
        }) 

        headers = {
            'content-type': 'application/json',
            'Authorization':f'Token {token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            response_data = json.loads(response.json())
            return JsonResponse({'status':'success'}, status=200)
             
        else :
            data = {
                'status': 'error',
                'message': 'Failed to update user',
            }

            return JsonResponse(data, status=400)


def delete_user_view(request):
    url = f"{base_url(request)}{reverse('delete_user_api')}"
    headers = {
        'Authorization':f'Token {request.session.get("token")}',
        'Content-Type': 'application/json',
    }
    if request.method == 'GET':
        return render(request,'users.html')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        payload = json.dumps({
            "user_id": user_id,
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            return JsonResponse({'status': 'success'}, status=200)
        else:
            return JsonResponse({'error': 'An error occurred while Deleting the user.'}, status=400)


def update_password(request):
    if request.method == 'POST':
        token =request.session.get("token")
        url = f'{base_url(request)}{reverse("update_password_api")}'
        new_password = request.POST.get('password')
        header ={
            'content-type':'application/json',
            'Authorization':f'Token {token}'}
        payload = json.dumps({
            'password':new_password,
        })
        response = requests.request('POST', url=url, data=payload, headers=header)
        response_data = json.loads(response.json())
        token = response_data.get('token') 
        return JsonResponse(data=response_data,status=200, safe=False)
       
