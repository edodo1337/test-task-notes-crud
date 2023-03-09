import pytest
from pytest_django.fixtures import SettingsWrapper
from pytest_django.lazy_django import skip_if_no_django
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from tests.factories import NoteFactory, ProfileFactory, UserFactory


@pytest.fixture(scope="session")
def settings():
    """A Django settings object which restores changes after the testrun"""
    skip_if_no_django()

    wrapper = SettingsWrapper()
    yield wrapper
    wrapper.finalize()


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def authorized_api_client__without_profile(api_client):
    user = UserFactory.create(username='testuser', password='testpass')
    token = AccessToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    return api_client


@pytest.fixture
def authorized_api_client__with_profile(api_client):
    user = UserFactory.create(username='testuser', password='testpass')
    profile = ProfileFactory.create(user=user)
    token = AccessToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    return api_client, profile


@pytest.fixture
def populate_notes_for_profile():
    def wrapper(profile):
        notes = NoteFactory.create_batch(size=5, author=profile)
        return notes

    return wrapper
