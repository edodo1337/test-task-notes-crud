from django.contrib.auth.models import User
from users.logic.exceptions import ProfileNotFound

from users.models import Profile
from loguru import logger


def profile__by_user(user: User) -> Profile:
    profile = Profile.objects.filter(user=user).first()
    if profile is None:
        logger.error(f"Profile not found by user_id={user.pk}")
        raise ProfileNotFound("Profile not found")
    return profile
