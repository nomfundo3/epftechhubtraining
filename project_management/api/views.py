from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from . serializer import (
    ProjectCreateSerializer,
    AssignClerkToProjectSerializer,
    ProjectUpdateSerializer,
    UserSerializer,
    ProjectSerializer,
    DeleteProjectSerializer,
    UserSerializer,
    UserTypeModelSerializer,
    CreateFormSerializer,
    FormFieldsSerializer

    )
from system_management import constants
from project_management.models import Form, Project, FormField
from system_management.models import Usertype,User
import json
import requests
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from system_management.api.base_url_mod import base_url


@api_view(['GET'])        
def fetch_user_api(request):
    if request.method == 'GET':
        user = request.user
        users = User.objects.filter(user_type_id__type = constants.CLERK).exclude(id=user.id)
        user_serializer = UserSerializer(instance=users, many=True)
        try:
            data = json.dumps({
                'status': 'success',
                'message': 'User details',
                'data': user_serializer.data,
            })
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            data = json.dumps({
                'status': 'error',
                'message': str(e),
            })
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def create_project_api_get(request):

    projects = Project.objects.all()
    serializer = ProjectSerializer(instance=projects, many=True)
    try:
        data = json.dumps({
            'status': 'success',
            'message': 'Project details',
            'data': serializer.data 
        })
        return Response(data=data, status=status.HTTP_200_OK)
    
    except Exception as e:
        data = json.dumps({
            'status': 'error',
            'message': str(e),
        })
        return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_project_api_post(request):
    body=json.loads(request.body)
    serializer = ProjectSerializer(data=body)
    if serializer.is_valid():
        name = serializer.validated_data.get('name')
        description = serializer.validated_data.get('description')     
        project = Project.objects.create(
            name=name,
            description=description,
        ) 
        
        created_date_formatted = project.date_created.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            'status': 'success',
            'message': 'Project created successfully',
            'created_date':  created_date_formatted
        }
        return Response(data, status=status.HTTP_201_CREATED)
    
    else:
        data = {
            'status': 'error',
            'message': serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_project_api(request):
     
    if request.method == 'POST':
        body = json.loads(request.body)
        serializer = ProjectUpdateSerializer(data=body)
        
        if serializer.is_valid():
            name = serializer.validated_data['name']
            description  = serializer.validated_data['description']
            project_id = serializer.validated_data['project_id']

            Project.objects.filter(id=project_id).update(
                name=name,
                description=description
            )

            
            data = json.dumps({
                'status': 'success',
                'message': 'Project updated successfully'
            })

            return Response(data=data, status=status.HTTP_200_OK)
        
        else:
            data = json.dumps({
                'status': 'error',
                'message': serializer.errors,
            })
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])  
def delete_project_api(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serializer = DeleteProjectSerializer(data=data)

            if serializer.is_valid():
                project_id = serializer.validated_data.get('project_id')
                try:
                    project_id = Project.objects.get(pk=project_id)
                    project_id.delete()
                    data = json.dumps({
                        'status': 'success',
                        'message': 'Project deleted successfully'
                    })
                    return Response(data, status=200)
                except Project.DoesNotExist:
                    data =json.dumps ({
                        'status': 'error',
                        'message': f'Project with ID {project_id} does not exist'
                    })
                    return Response(data, status=404)
            else:
                return Response(serializer.errors, status=400)
            
        except json.JSONDecodeError:
            data = json.dumps({
                'status': 'error',
                'message': 'Invalid JSON data in the request body'
            })
            return Response(data, status=400)
    else:
        data = json.dumps({
            'status': 'error',
            'message': 'Method Not Allowed'
        })
        return Response(data, status=405)
    

@api_view(['POST'])
def create_form_api(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        serializer = CreateFormSerializer(data=body)
        
        if serializer.is_valid():
           form_name = serializer.validated_data.get('form_name')
           field_name_list = serializer.validated_data.get('field_name_list')

        else:
            data = json.dumps({
                'status': "error",
                'message': serializer.errors
            })
            return Response(data=data, status=400) 
        
        form=Form.objects.create(
                form_name=form_name
            )
        form_id=form.id
        
        form_field_list = [
            FormField(
                field_type = True,
                field_name = field,
                field_required = True,
                form_id = form_id
            )
            for field in field_name_list
        ]
        FormField.objects.bulk_create(form_field_list)
        data = json.dumps({
            'status':   'success',
            'message': 'Form created successfully'
        })
    return Response(data, status=200)
    
        
        
		
		


	
        
        
	
       
