from django.urls import reverse
import pytest
from notes.models import Note

from tests.factories import NoteFactory, ProfileFactory, UserFactory


NOTES_LIST_URL = reverse('note-list')
NOTE_DETAIL_URL = lambda pk: reverse('note-detail', kwargs={'pk': pk})


@pytest.mark.django_db
def test__notes_list__unauthorized(api_client):
    resp = api_client.get(path=NOTES_LIST_URL)

    assert resp.status_code == 401


@pytest.mark.django_db
def test__notes_list__empty(authorized_api_client__with_profile):
    client, _ = authorized_api_client__with_profile
    resp = client.get(path=NOTES_LIST_URL)
    data = resp.json()

    assert resp.status_code == 200
    assert data['count'] == 0
    assert len(data['results']) == 0


@pytest.mark.django_db
def test__notes_list__owner_only(authorized_api_client__with_profile, populate_notes_for_profile):
    client, profile1 = authorized_api_client__with_profile
    profile2 = ProfileFactory.create(user=UserFactory.create())
    notes1 = populate_notes_for_profile(profile1)
    populate_notes_for_profile(profile2)

    resp = client.get(path=NOTES_LIST_URL)
    data = resp.json()

    assert resp.status_code == 200
    assert data['count'] == len(notes1)
    assert len(data['results']) == len(notes1)
    for note_resp, note in zip(data['results'], notes1):
        note_resp['pk'] == note.pk
        note_resp['title'] == note.title
        note_resp['description'] == note.description


@pytest.mark.django_db
def test__note_create(authorized_api_client__with_profile):
    client, profile = authorized_api_client__with_profile
    content = {"title": "test-title", "description": "test-description"}

    resp = client.post(path=NOTES_LIST_URL, data=content)
    data = resp.json()
    note = Note.objects.first()

    assert note is not None
    assert resp.status_code == 201
    assert data['title'] == content['title']
    assert data['description'] == content['description']
    assert data['created_at'] is not None
    assert data['pk'] == note.pk
    assert data['author'] == profile.pk


@pytest.mark.django_db
def test__note_update(authorized_api_client__with_profile):
    client, profile = authorized_api_client__with_profile
    note = NoteFactory.create(author=profile)
    content = {"title": "test-title", "description": "test-description"}

    resp = client.put(path=NOTE_DETAIL_URL(note.pk), data=content)
    data = resp.json()
    note = Note.objects.first()

    assert note is not None
    assert resp.status_code == 200
    assert data['title'] == content['title']
    assert data['description'] == content['description']
    assert data['created_at'] is not None
    assert data['pk'] == note.pk
    assert data['author'] == profile.pk


@pytest.mark.django_db
def test__note_delete(authorized_api_client__with_profile):
    client, profile = authorized_api_client__with_profile
    note = NoteFactory.create(author=profile)

    resp = client.delete(path=NOTE_DETAIL_URL(note.pk))
    note = Note.objects.filter(pk=note.pk).first()

    assert note is None
    assert resp.status_code == 200
