from notes.enums import NotesResponseCodes
from rest_framework import status

from notes.logic.exceptions import NoteNotFound


def get_status_code_by_error(error_code: NotesResponseCodes) -> str:
    error_codes_map = {NotesResponseCodes.NOTE_NOT_FOUND.value: status.HTTP_404_NOT_FOUND}

    return error_codes_map.get(error_code, status.HTTP_400_BAD_REQUEST)


def get_error_code(exc: Exception) -> NotesResponseCodes:
    if isinstance(exc, NoteNotFound):
        return NotesResponseCodes.NOTE_NOT_FOUND
    return NotesResponseCodes.DEFAULT
