import datetime
from pytest_factoryboy import register
from django.contrib.auth.models import User

from users.models import Profile
from notes.models import Note
from factory.fuzzy import FuzzyDate, FuzzyText
from factory.django import DjangoModelFactory


@register
class ProfileFactory(DjangoModelFactory):
    birth_date = FuzzyDate(start_date=datetime.date(year=2000, month=1, day=1))
    full_name = FuzzyText(length=10)

    class Meta:
        model = Profile


@register
class NoteFactory(DjangoModelFactory):
    title = FuzzyText(length=10)
    description = FuzzyText(length=10)

    class Meta:
        model = Note


@register
class UserFactory(DjangoModelFactory):
    username = FuzzyText(length=10)

    class Meta:
        model = User
