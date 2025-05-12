from django.db.models import fields
from rest_framework import serializers
from project_management.models import Project,Form
from system_management.models import User , Usertype

class ProjectCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    form_id = serializers.IntegerField()  
    

class ProjectUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    project_id=serializers.CharField()
   

class UserTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usertype
        fields = ('id', 'type')

class UserSerializer(serializers.ModelSerializer):
    user_type__type = serializers.SerializerMethodField()
    phone_number__profile = serializers.SerializerMethodField()

    @staticmethod
    def get_phone_number__profile(obj):
        return obj.profile.phone_number

    @staticmethod
    def get_user_type__type(obj):
        """
        Get the user type

        :param obj:
            User object
        :return:
            From Foreign key user type access model User Type to get type field.
        """
        return obj.user_type.type  

    class Meta:
        """Metaclass for user model serializer"""
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email', 
            'user_type_id',
            'user_type__type',
            'phone_number__profile',
            )
       

class AssignClerkToProjectSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    clerk_id = serializers.IntegerField()

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id','name' ,'description','form','date_created']


class DeleteProjectSerializer(serializers.Serializer):
    project_id = serializers.CharField()

class CreateFormSerializer(serializers.ModelSerializer):
    form_name= serializers.CharField(max_length=100)
    field_name_list = serializers.ListField(child=serializers.CharField(max_length=100))


    class Meta:
        model = Form
        fields = ['form_name','field_name_list']



class FormFieldsSerializer(serializers.Serializer):
    form_fk__id = serializers.SerializerMethodField()

    def get_form_fk__id(self, obj):
        return obj.form_fk.id if obj.form_fk else None





