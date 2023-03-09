from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist


class IsAuthenticatedAndHasProfile(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        try:
            request.user.profile
        except ObjectDoesNotExist:
            self.message = "User has no profile"
            return False
        return True
