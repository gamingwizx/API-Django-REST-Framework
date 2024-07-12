from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

class AdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        username = request.user.username
        admin_permission = bool(request.user and request.user.is_staff)
        return request.method == 'POST'  and admin_permission

class SpecialPermission1(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.method == 'POST':
            return request.user

class SpecialPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        token_string = request.META.get('HTTP_AUTHORIZATION')
        if token_string is None:
            if request.method == "GET":
                return True
            return False

        token = request.META.get('HTTP_AUTHORIZATION').split("Token ",1)[1]

        token = Token.objects.select_related("user").get(key=token)
        self.user = token.user

        if (request.method == 'POST' or request.method == "PUT" or request.method == "DELETE") and self.user.is_staff:
            return True
        
        if (request.method == "GET"):
            return True
        return False
        
    
class AuthorizeCreate(permissions.BasePermission):
    def has_permission(self, request,view):
        return view.action == "create" and request.user and request.user.is_authenticated    

class permission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user.is_staff)
        
class isDataOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user
    
class isDataOwnerWhenUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #Check if object has permisisons when perform update
        if ((request.method == "PUT" or request.method == "DELETE") and (obj.reviewer == request.user)):
            return True
        
        if (request.method == "GET"):
            return True
        
        return False
        