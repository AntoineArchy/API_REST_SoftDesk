from rest_framework import permissions

class IsContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.contributors.all()

class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
