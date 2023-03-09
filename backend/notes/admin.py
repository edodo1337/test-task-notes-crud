from django.contrib import admin

from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "created_at", "get_author_name")

    @admin.display(ordering='author__full_name', description='Note author')
    def get_author_name(self, obj):
        return obj.author.full_name
