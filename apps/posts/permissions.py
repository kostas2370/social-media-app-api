from rest_framework.permissions import BasePermission


class PostPermissions(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if not request.user.is_verified:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ["like", "dislike", "comment", "retrieve"]:
            return not(request.user not in obj.author.friends.all() and
                       not obj.author.is_public and
                       not obj.author == request.user)

        return not obj.author != request.user




