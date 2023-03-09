from rest_framework.permissions import IsAuthenticated

from notes.models import Note


class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj: Note):
        if not super().has_object_permission(request, view, obj):
            return False

        if not (request.user and request.user.is_authenticated or request.user.is_staff):
            return False

        if obj.author != request.user.profile:
            return False

        return True
