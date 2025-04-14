from core.permissions import BaseCorePermission

class IsOwnerPermission(BaseCorePermission):
    message = "You must be the owner of this object to perform this action."
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user