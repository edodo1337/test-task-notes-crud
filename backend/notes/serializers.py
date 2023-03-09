from dataclasses import dataclass
from rest_framework import serializers
from rest_framework_dataclasses.serializers import DataclassSerializer
from notes.dto import NoteDTO

from notes.models import Note


class NoteListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('pk', 'title', 'description', 'author')


class NoteCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()


class NoteUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_null=False, allow_blank=False)
    description = serializers.CharField(required=False, allow_null=False, allow_blank=False)


class NoteSerializer(DataclassSerializer):
    class Meta:
        dataclass = NoteDTO


@dataclass
class NoteCreateErrorResposne:
    error_msg: str
    error_code: str


class NoteCreateErrorSerializer(DataclassSerializer):
    class Meta:
        dataclass = NoteCreateErrorResposne
