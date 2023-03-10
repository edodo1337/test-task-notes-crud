from dataclasses import asdict
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from notes.logic.interactors import create_note, delete_note, update_note
from notes.models import Note
from drf_yasg.utils import swagger_auto_schema
from notes.permissions import IsOwner

from notes.serializers import (
    NoteCreateErrorSerializer,
    NoteCreateSerializer,
    NoteListItemSerializer,
    NoteSerializer,
    NoteUpdateSerializer,
)
from notes.utils import get_error_code, get_status_code_by_error
from users.logic.selectors import profile__by_user
from users.permission import IsAuthenticatedAndHasProfile
from utils import catch_exception_factory


catch_exception = catch_exception_factory(get_error_code, get_status_code_by_error)


class NotesViewSet(ListAPIView, RetrieveAPIView, ViewSet):
    serializer_class = NoteListItemSerializer
    permission_classes = (IsAuthenticatedAndHasProfile | IsOwner,)
    queryset = Note.objects.all()

    @swagger_auto_schema(
        request_body=NoteCreateSerializer,
        responses={
            status.HTTP_201_CREATED: NoteSerializer,
            status.HTTP_404_NOT_FOUND: NoteCreateErrorSerializer,
            status.HTTP_400_BAD_REQUEST: NoteCreateErrorSerializer,
        },
    )
    @catch_exception
    def create(self, request: Request, *args, **kwargs):
        serializer = NoteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        author = profile__by_user(self.request.user)
        note_dto = create_note(author=author, title=data['title'], description=data['description'])

        return Response(data=asdict(note_dto), status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=NoteUpdateSerializer,
        responses={
            status.HTTP_200_OK: NoteSerializer,
            status.HTTP_404_NOT_FOUND: NoteCreateErrorSerializer,
            status.HTTP_400_BAD_REQUEST: NoteCreateErrorSerializer,
        },
    )
    @catch_exception
    def update(self, request: Request, pk: int):
        note = self.get_object()
        serializer = NoteUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        note_dto = update_note(note=note, **data)

        return Response(data=asdict(note_dto), status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_404_NOT_FOUND: NoteCreateErrorSerializer,
            status.HTTP_400_BAD_REQUEST: NoteCreateErrorSerializer,
        }
    )
    def destroy(self, request: Request, pk: int):
        note = self.get_object()
        delete_note(note=note)

        return Response(data={"status": True}, status=status.HTTP_200_OK)

    def get_queryset(self):
        if not hasattr(self.request.user, 'profile'):
            return Note.objects.none()
        return Note.objects.filter(author=self.request.user.profile)
