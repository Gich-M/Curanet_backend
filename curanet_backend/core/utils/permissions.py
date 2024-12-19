from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
class IsPharmacist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'pharmacist'
    
class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'
    
class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'patient'
    
class CanManageInventory(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin'or request.user.role == 'pharmacist'\
                or request.user.role == 'doctor')

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allow patients to view or update their own data while
        allowing admins to access all the data.
    """
    def has_permission(self, request, view, obj):
        if request.user.role  == 'patient' and obj.user == request.user:
            return True
        return request.user.role == 'admin'
    
