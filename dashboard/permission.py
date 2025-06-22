from rest_framework.permissions import BasePermission, IsAuthenticated

class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method=='GET':
            return True
        return bool(request.user and request.user.is_authenticated)
    
    def has_permission(self, request, view):
        if request.method=='GET':
            return True
        return bool(request.user and request.user.is_authenticated)
