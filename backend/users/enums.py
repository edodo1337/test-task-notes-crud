from enum import Enum


class ProfilesResponseCodes(str, Enum):
    PROFILE_NOT_FOUND = "PROFILE_NOT_FOUND"
    PASSWORDS_DOESNT_MATCH = "PASSWORDS_DOESNT_MATCH"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    DEFAULT = "DEFAULT"
