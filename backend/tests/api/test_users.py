import datetime
from django.urls import reverse
import pytest

from users.models import Profile


PROFILE_REGISTER_URL = reverse('profile-register')


@pytest.mark.django_db
def test__profile_register(api_client):
    content = {
        'full_name': 'test-name',
        'birth_date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'username': 'test-user',
        'email': 'test@test.com',
        'password': 'secretpass123',
    }

    resp = api_client.post(path=PROFILE_REGISTER_URL, data=content)
    data = resp.json()

    profile = Profile.objects.last()
    assert resp.status_code == 201, data
    assert profile.full_name == content['full_name']
    assert profile.user.username == content['username']
