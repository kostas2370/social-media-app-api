from rest_framework.permissions import BasePermission
from apps.usersapp import utils


class UniversityPermissions(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return request.user.is_verified
    def has_object_permission(self, request, view, obj):
        if obj.admin == request.user:
            return True

        if view.action in ["destroy", "partial_update", "patch", "post"]:
            return False

        return obj.is_active


class ReviewPermission(BasePermission):
    message = 'Not same email domain'

    def has_object_permission(self, request, view, obj):
        if view.action == "review":
            return utils.check_if_university_domain(request.user.email) == obj.id

        return True
