from django.contrib.auth.models import update_last_login
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from django.db import transaction
from django.conf import settings
from django.db.models import Q

from rest_framework import (serializers, status)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import TokenError


from .utils import generate_username, User


class MainRegisterSerializer(serializers.Serializer):
    token_class = RefreshToken
    status_code = serializers.IntegerField(read_only=True, default=status.HTTP_400_BAD_REQUEST)
    status = serializers.BooleanField(read_only=True, default=False)
    message = serializers.CharField(read_only=True, default =None)
    data = serializers.DictField(read_only=True, default = None)
    
    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resp = {
            'status' : False,'status_code' : status.HTTP_400_BAD_REQUEST,
            'message': None,'data' : None
        }
        self.fields['first_name'] = serializers.CharField(max_length= 100, required = True,write_only=True)
        self.fields['last_name'] = serializers.CharField(max_length=100, required = False,write_only=True)
        self.fields['email'] = serializers.EmailField(required=True,write_only=True) #,validators=[UniqueValidator(queryset=User.objects.all())]
        self.fields['password'] = serializers.CharField(write_only=True, required=True)#, validators=[cus_password_validator]
        if settings.ENABLE_CONFIRM_PASSWORD == True:
            self.fields['confirm_password'] = serializers.CharField(write_only=True, required=True)
        if settings.USER_DEFINED_USERNAME == True:
            self.fields['username'] = serializers.CharField(max_length=100, required = True,write_only=True)

    def validate(self, attrs):
        errors = None
        password = attrs['password']
        email = attrs['email']
        attrs['valid'] = False
        special_characters = r'!"\#$%&()*+,-./:;<=>?@[\\]^_`{|}~\'•√π÷×§∆£¢€¥°©®™✓'
        is_valid = True
        if settings.USER_DEFINED_USERNAME == True:
            username = attrs['username']
            if is_valid and User.objects.filter(username=username).exists():
                errors = "This username is already taken."
                is_valid = False
        if is_valid and User.objects.filter(email=email).exists():
            errors = "This email is already taken."
            is_valid = False
        if settings.ENABLE_CONFIRM_PASSWORD == True:
            password2 = attrs['confirm_password']
            if is_valid and password != password2:
                errors = "Password fields didn’t match."
                is_valid = False
        if is_valid and not any(char.islower() for char in password):
            errors = "Password must contain at least one lowercase letter."
            is_valid = False
        if is_valid and not any(char.isupper() for char in password):
            errors = "Password must contain at least one uppercase letter."
            is_valid = False
        if is_valid and not any(char in special_characters for char in password):
            errors = "Password must contain at least one Special character."
            is_valid = False
        
        if not is_valid:
            attrs['error'] = errors
        attrs['valid'] = is_valid
        return attrs
    
    def create(self, validated_data):
        print("validated_data:", validated_data)
        if validated_data['valid'] == True:
            first_name = validated_data.get('first_name',None)
            last_name = validated_data.get('last_name',None)
            username = validated_data.get('username',None)
            email = validated_data.get('email',None)
            password = validated_data.get('password',None)
            if settings.USER_DEFINED_USERNAME == False:
                if settings.EMAIL_AS_USERNAME == True:
                    username = email
                else:
                    username = generate_username(first_name, last_name)
            user_dict = {
                "username" : username,
                "email" : email,
                "first_name" : first_name
            }
            if last_name is not None:
                user_dict['last_name'] = last_name
            with transaction.atomic():
                user_obj = User(**user_dict)
                user_obj.set_password(password)
                user_obj.save()
                self.resp['status'] = True 
                self.resp['status_code'] = status.HTTP_201_CREATED
                self.resp['message'] = 'User created successfully'
                self.resp["data"] = {'email' : user_obj.email}
                if settings.LOGIN_ON_REGISTRATION == True:
                    refresh = self.get_token(user_obj)
                    self.resp['data'].update({"access" : str(refresh.access_token),"refresh" : str(refresh),})
        else:
            self.resp['message'] = validated_data.get('error')
        return self.resp
    

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields["username"] = serializers.CharField(required = True)
        self.fields["password"] = serializers.CharField(required = True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        try:
            user_obj = User.objects.get(Q(email=username)|Q(username=username))
        except User.DoesNotExist as e:
            user_obj =  None
        if user_obj is not None:
            authenticate_kwargs = {
                "username": user_obj.username,
                "password": password,
            }
            print("authenticate_kwargs",authenticate_kwargs)
            try:
                authenticate_kwargs["request"] = self.context["request"]
            except KeyError:
                pass

            self.user = authenticate(**authenticate_kwargs)
            print("self.user", self.user)
            if not api_settings.USER_AUTHENTICATION_RULE(self.user):
                return {'message': 'Invalid password'}
            else:
                data = {
                    'name' :self.user.first_name,
                    'email' : self.user.email
                }
                return data 
        else:
            return {'message': 'Invalid email or username'}
        
    @classmethod
    def get_token(cls, user):
        return super().get_token(user)


class CustomTokenObtainPairSerializer(MyTokenObtainPairSerializer):
    token_class = RefreshToken
    def validate(self, attrs):
        response = {"status" : False,"status_code"  : None, "message" : None, "data" : None}
        data = super().validate(attrs)
        if 'message' not in data.keys():
            print(data)
            refresh = self.get_token(self.user)
            response["status"] = True
            
            response["status_code"] = status.HTTP_200_OK
            response["message"] = "Login Successfully"
            response["data"] = data
            response['data']["refresh"] = str(refresh)
            response['data']["access"] = str(refresh.access_token)
            
            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, self.user)
        else:
            response["status"] = False
            response["message"] = data["message"]
            response["status_code"] = status.HTTP_400_BAD_REQUEST
        return response

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            token = RefreshToken(self.validated_data['refresh'])
            token.blacklist()
        except TokenError:
            self.fail('bad_token')
            return { 'bad_token': 'Token is expired or invalid'}