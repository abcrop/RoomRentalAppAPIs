from rest_framework import permissions
import logging

from rest_framework.exceptions import APIException, PermissionDenied

logger = logging.getLogger(__name__)
del logging

"""
IsAdminAndLandLoardOrReadOnly is responsible for:
- allowing only LandLord and  Admin to POST, PUT, DELETE
- anyone can GET
"""

class IsAdminOrLandLordAndReadOnly(permissions.BasePermission):
    message = 'You are not athorized.'
    
    """
    Global permissions that run against all incoming requests.
    Header value validation.
    eg: Blocking IP address
    
    has_permission: GET,POST,PUT,DELETE,OPTION 
    """
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            try:
                logger.debug(f"user_type: {request.user.user_type} ")
            
                if request.user.user_type == 'LL' or request.user.user_type == 'AD':
                    return True
                else:
                    self.message = "Tenant don't have permission to this action."
                    return False
                
            except Exception as e:
                raise PermissionDenied()
                    
        return True
            
    
    """
    Object Level Permission, that run against operations that affect a particular object instance
    
    """
    
    def has_object_permission(self, request, view, obj):
        """
        GET, HEAD, OPTION
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        
        else:
            """
            PUT,DELETE,RETRIEVE
            """
        
            #Owner and Admin only can change the object in db
            isOwnerOrAdmin = False
            
            try:
                if obj.owner_id.id == request.user.id or request.user.user_type == "AD":
                    isOwnerOrAdmin = True
                    return isOwnerOrAdmin
                
            except Exception as e:
                if obj.id:
                    if obj.id == request.user.id or request.user.user_type == "AD":
                        isOwnerOrAdmin = True
                        return isOwnerOrAdmin
                    return isOwnerOrAdmin
                else:
                    if obj.room_id.owner_id == request.user or request.user.user_type == "AD":
                        isOwnerOrAdmin = True
                        return isOwnerOrAdmin
                    return isOwnerOrAdmin

"""
IsAdminAndTenantOrReadOnly is responsible for:
- allowing only Tenant and  Admin to POST, PUT, DELETE
- anyone can GET
"""
class IsAdminOrTenantAndReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.method == 'POST':
                if request.user.user_type == 'AD' or request.user.user_type == 'TN':
                    return True
                else:
                    return False
                
        except Exception as e:
            raise False
            
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        else:
            isAdminOrTenant = False
            
            try:
                if request.user.id == obj.tenant_id.id or request.user.user_type == 'AD':
                    isAdminOrTenant = True
                    return isAdminOrTenant
                else:
                    isAdminOrTenant = False
                    return isAdminOrTenant
                
            except Exception as e:
                return False

"""
IsAdminOrReadOnly is responsible for:
- allowing only resource admin to POST
- anyone can GET
"""

class IsAdminAndReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':    
            try:
                if request.user.user_type == 'AD':
                    return True
                else:
                    return False
            except Exception as e:
                return False
        return True
            
"""
IsAdminAndResourceOwnerOnly is responsible for:
- allowing only resource Owner AND Admin to RETRIEVE,PUT, DELETE object instance
- 
"""
        
class IsAdminOrResourceOwnerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
            
    """
    has_object_permission is only about: retrieve, put
    """
    def has_object_permission(self, request, view, obj):
        """
        GET refers to: list [ rooms/]->post [], retrieve [rooms/1]->put []
        """
        isAdminAndOwner = False
        
        if request.method:
            if request.user.id == obj.id or request.user.user_type == 'AD':
                isAdminAndOwner = True
                return isAdminAndOwner
            return isAdminAndOwner
        return isAdminAndOwner
    
    