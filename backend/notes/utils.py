from dataclasses import asdict
from typing import Callable
from notes.enums import NotesResponseCodes
from rest_framework import status
from rest_framework.serializers import ValidationError

from notes.logic.exceptions import NoteNotFound
from notes.serializers import NoteCreateErrorResposne
from rest_framework.response import Response


def get_status_code_by_error(error_code: NotesResponseCodes) -> str:
    if error_code == NotesResponseCodes.NOTE_NOT_FOUND.value:
        return status.HTTP_404_NOT_FOUND
    return status.HTTP_400_BAD_REQUEST


def get_error_code(exc: Exception) -> NotesResponseCodes:
    if isinstance(exc, NoteNotFound):
        return NotesResponseCodes.NOTE_NOT_FOUND
    return NotesResponseCodes.DEFAULT


def catch_exception(view: Callable):
    def wrapper(*args, **kwargs):
        try:
            return view(*args, **kwargs)
        except ValidationError as ex:
            raise ex
        except Exception as ex:
            error_code = get_error_code(ex)
            status_code = get_status_code_by_error(error_code)

            return Response(
                data=asdict(NoteCreateErrorResposne(error_msg=str(ex), error_code=error_code)),
                status=status_code,
            )

    return wrapper
