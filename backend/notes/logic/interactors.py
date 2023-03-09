from notes.dto import NoteDTO
from notes.models import Note
from users.models import Profile


def create_note(*, author: Profile, title: str, description: str) -> NoteDTO:
    new_note = Note.objects.create(author=author, title=title, description=description)

    return NoteDTO(
        title=new_note.title,
        description=new_note.description,
        created_at=new_note.created_at,
        author=new_note.author.pk,
        pk=new_note.pk,
    )


def update_note(*, note: Note, title: str | None = None, description: str | None = None) -> NoteDTO:
    note.title = title or note.title
    note.description = description or note.description
    note.save()

    return NoteDTO(
        title=note.title,
        description=note.description,
        created_at=note.created_at,
        author=note.author.pk,
        pk=note.pk,
    )


def delete_note(*, note: Note):
    note.delete()
