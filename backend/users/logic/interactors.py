import datetime
from users.logic.exceptions import PasswordDoesNotMatch
from users.models import Profile
from django.contrib.auth.models import User


def create_profile(
    *, full_name: str, birth_date: datetime.datetime, email: str, username: str, password: str
) -> Profile:
    user = User.objects.create(username=username, password=password, email=email)
    profile = Profile.objects.create(user=user, full_name=full_name, birth_date=birth_date)

    return profile


def update_profile(
    *,
    profile: Profile,
    full_name: str | None = None,
    birth_date: datetime.datetime | None = None,
    password: str | None = None,
    password_2: str | None = None,
) -> Profile:
    user = profile.user
    profile.full_name = full_name or full_name.full_name
    profile.birth_date = birth_date or profile.birth_date
    if password is not None and password_2 is not None:
        if password != password_2:
            raise PasswordDoesNotMatch

        user.set_password(password)
        user.save()

    profile.user = user
    profile.save()

    return profile
