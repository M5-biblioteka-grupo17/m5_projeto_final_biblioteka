from rest_framework import permissions

class IsLibraryCollaboratorOrOwner(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return(
            request.user.is_authenticated and
            request.user.library_collaborator or
           ( request.user.is_authenticated and obj.email == request.user.email)
        )