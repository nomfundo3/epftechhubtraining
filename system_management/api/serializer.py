from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from system_management.models import Profile, Otp
from system_management.models import User
from system_management.models import Profile, Otp, Usertype

class UserLoginBaseSerialize(serializers.Serializer):
    username = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=50)

class UserCountSerializer(serializers.Serializer):
    user_count = serializers.IntegerField()
class OtpSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)
   

class OtpBaseSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length = 4)

class UserEditProfileBaseSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    phone_number = serializers.CharField(max_length=10, required=True)
    gender = serializers.CharField(max_length=50, required=True)
    identity_number = serializers.CharField(max_length=13,allow_null=True)
    passport_number = serializers.CharField(max_length=9,allow_null=True)
    ethnicity = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=255)
    date_of_birth = serializers.CharField(max_length=25)


class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100) 

class ProfileModalSerializer(serializers.ModelSerializer):
    user_fk__first_name = serializers.SerializerMethodField()
    user_fk__last_name = serializers.SerializerMethodField()
    user_fk__email = serializers.SerializerMethodField()
    
    @staticmethod
    def get_user_fk__first_name(obj):
        return obj.user.first_name

    @staticmethod
    def get_user_fk__last_name(obj):
        return obj.user.last_name
    
    @staticmethod
    def get_user_fk__email(obj):
        return obj.user.email

    class Meta:
        model = Profile
        fields = (
            'id',
            'phone_number',
            'gender',
            'user_id',
            'passport_number',
            'identity_number',
            'date_of_birth',
            'ethnicity',
            'address',
            'user_fk__first_name',
            'user_fk__last_name',
            'user_fk__email'
            )

class UserRegistrationBaseSerialize(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=15)
    user_type = serializers.IntegerField(required=True)

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usertype
        fields = ('id', 'type')

class UserSerialize(serializers.ModelSerializer):
    user_type__type = serializers.SerializerMethodField()
    phone_number__profile = serializers.SerializerMethodField()

    @staticmethod
    def get_phone_number__profile(obj):
        try:
            profile = Profile.objects.get(user_id=obj.id)
            phone_number = profile.phone_number
        except Profile.DoesNotExist:
            phone_number = ''
        return phone_number

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

       
class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'phone_number')        

class UserTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usertype
        fields = ('id', 'type') 

class UserUpdateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    phone_number = serializers.CharField(required=True, max_length=15)
        
class DeleteUserSerializer(serializers.Serializer):
    user_id = serializers.CharField()

