from rest_framework.permissions import BasePermission, SAFE_METHODS

class isCollaboratorOrGet(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.library_collaborator
    
class isCollaborator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.library_collaborator