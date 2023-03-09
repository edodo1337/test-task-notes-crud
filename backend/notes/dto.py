import datetime
from dataclasses import dataclass


@dataclass
class NoteDTO:
    title: str
    description: str
    created_at: datetime.datetime
    author: int
    pk: int
