from rest_framework.permissions import BasePermission

class isCollaboratorOrGet(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return request.user.is_authenticated and request.user.library_collaborator