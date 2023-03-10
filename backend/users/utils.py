from rest_framework import status

from users.enums import ProfilesResponseCodes
from users.logic.exceptions import PasswordDoesNotMatch, ProfileNotFound, UserAlreadyExists


def get_status_code_by_error(error_code: ProfilesResponseCodes) -> str:
    error_codes_map = {
        ProfilesResponseCodes.PROFILE_NOT_FOUND.value: status.HTTP_404_NOT_FOUND,
        ProfilesResponseCodes.PASSWORDS_DOESNT_MATCH.value: status.HTTP_400_BAD_REQUEST,
        ProfilesResponseCodes.USER_ALREADY_EXISTS.value: status.HTTP_400_BAD_REQUEST,
    }

    return error_codes_map.get(error_code, status.HTTP_400_BAD_REQUEST)


def get_error_code(exc: Exception) -> ProfilesResponseCodes:
    if isinstance(exc, ProfileNotFound):
        return ProfilesResponseCodes.NOTE_NOT_FOUND
    elif isinstance(exc, PasswordDoesNotMatch):
        return ProfilesResponseCodes.PASSWORDS_DOESNT_MATCH
    elif isinstance(exc, UserAlreadyExists):
        return ProfilesResponseCodes.USER_ALREADY_EXISTS

    return ProfilesResponseCodes.DEFAULT
