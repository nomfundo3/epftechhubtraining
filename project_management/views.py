from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
import requests
import json
from django.http import HttpResponse
from django.contrib import messages
from .models import Project


def base_url(request):
    protocol = request.scheme
    host = request.get_host()
    host_url = f'{protocol}://{host}'
    return host_url


def fetch_user_view(request):
    token = request.session.get('token')
    url = f'{base_url(request)}{reverse("fetch_user_api")}'
    headers = {
            'content-type': 'application/json',
            'Authorization':f'Token {token}'
    }
    payload = json.dumps({})
    response = requests.request(method="GET", url=url , headers=headers, data=payload)
    response_data = json.loads(response.json())
    context ={
        'users':response_data['data'],
    }
    return render(request, 'create_project.html', context)


def create_project_view(request):
     
     if request.method == 'GET': 
        token = request.session.get('token')   
          
        if token is None:
            return redirect('create_project_view')
        
        url = f'{base_url(request)}{reverse("create_project_api_get")}'
        
        payload = json.dumps({})

        headers = {
            'content-type': 'application/json',
            'Authorization':f'Token {token}'
        }
        response = requests.request(method="GET", url=url , headers=headers, data=payload)   
        
        if response.status_code == 200:
            projects = json.loads(response.content)
            projects = json.loads(projects)
            context = {
                'projects': projects['data'],
                }

        return render(request, 'create_project.html',context)


     if request.method == "POST":
        token = request.session.get('token')
    
        name = request.POST.get('name')
        description = request.POST.get('description')
        form_id=request.POST.get('form_id')
    
        url = f'{base_url(request)}{reverse("create_project_api_post")}'
      
        payload = json.dumps({
            "name":name,
            "description":description,
            "form_id":form_id
        })

        headers = {
            'content-type': 'application/json',
            'Authorization': f'Token {token}'
        }

        response = requests.request(method="POST", url=url, headers=headers, data=payload)
        
        if response.status_code == 201:
            response_data = {'status':'success',"message": "Project created successfully"}
            return JsonResponse(response_data,status=201) 

        else:
             data = {
                'status': 'Error creating the project. Please try again.',
                'message': 'Failed to create the Project',
            }
             
        return JsonResponse(data, status=400)  
     return render(request, 'create_project.html')


def update_project_view(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        description = request.POST.get('description')
        project_id = request.POST.get('project_id')

        url = f'{base_url(request)}{reverse("update_project_api")}'

        payload = json.dumps({
            "name": name,
            "description": description,
            "project_id": project_id
        })

        headers = {
            'content-type': 'application/json',
            'Authorization':f'Token {request.session.get("token")}',
        
        }

        response = requests.request(method="POST",url=url, headers=headers, data=payload)
        
        if response.status_code == 200:
           response_data = json.loads(response.json())
            
           return JsonResponse({'status':'success'}, status=200)
        else:
            data = {
                'status': 'Error updating the project. Please try again.',
                'message': 'Failed to update the Project',
            }
            return JsonResponse(data, status=400)
    

def delete_project_view(request):
    url = f"{base_url(request)}{reverse('delete_project_api')}"
    headers = {
        'Authorization':f'Token {request.session.get("token")}',
        'Content-Type': 'application/json',
        }
    if request.method == 'GET':
        return render(request,'create_project.html')
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        payload = json.dumps({
            "project_id": project_id,
            })
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            data = {
              'status':'success' ,
            }
            return JsonResponse(data,safe=False, status=200)
            
        else:
            data = {'error':'An error occurred while Deleting the project.' }
            return JsonResponse(data,safe=False, status=400)
        

def create_form_view(request):
    if request.method == 'GET':
        return render(request,'create_form.html')
    
    if request.method == 'POST':
        form_name = request.POST.get('form_name')
        field_name_list  = request.POST.get('field_name_list')
        url = f"{base_url(request)}{reverse('create_form_api')}"
        headers = {
            'Authorization':f'Token {request.session.get("token")}',
            'Content-Type': 'application/json',
            }
        payload = json.dumps({
            "form_name": form_name,
            "field_name_list": field_name_list,
            })
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 201:
            data = {
              'status':'success' ,
            }
            return JsonResponse(data,safe=False, status=200)
            
        else:
            data = {'error':'An error occurred while creating the form.' }
            return JsonResponse(data,safe=False, status=400)
    return render(request,'create_form.html')

        

    
