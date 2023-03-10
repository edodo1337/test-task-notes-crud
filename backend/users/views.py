from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from users.logic.interactors import create_profile, update_profile
from users.logic.selectors import profile__by_user

from users.models import Profile
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from users.permission import IsAuthenticatedAndHasProfile

from users.serializers import ProfileCreateSerializer, ProfileSerializer, ProfileUpdateSerializer
from users.utils import get_error_code, get_status_code_by_error
from utils import catch_exception_factory


catch_exception = catch_exception_factory(get_error_code, get_status_code_by_error)


class ProfileViewSet(GenericAPIView, ViewSet):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticatedAndHasProfile,)
    pagination_class = None

    @swagger_auto_schema(responses={status.HTTP_200_OK: ProfileSerializer})
    @catch_exception
    @action(methods=["GET"], detail=False)
    def me(self, request: Request, *args, **kwargs):
        profile = profile__by_user(user=request.user)

        return Response(data=ProfileSerializer(instance=profile).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ProfileCreateSerializer, responses={status.HTTP_201_CREATED: ProfileSerializer}
    )
    @catch_exception
    @action(methods=["POST"], detail=False, permission_classes=(AllowAny,))
    def register(self, request: Request, *args, **kwargs):
        serializer = ProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        profile = create_profile(**data)

        return Response(
            data=ProfileSerializer(instance=profile).data, status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        request_body=ProfileUpdateSerializer, responses={status.HTTP_200_OK: ProfileSerializer}
    )
    @catch_exception
    @action(methods=["PATCH"], detail=False)
    def update_profile(self, request: Request):
        profile = request.user.profile
        serializer = ProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        profile = update_profile(profile=profile, **data)

        return Response(data=ProfileSerializer(instance=profile).data, status=status.HTTP_200_OK)
