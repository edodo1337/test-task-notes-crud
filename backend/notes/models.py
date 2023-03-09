from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Updated at", auto_now=True)

    class Meta:
        abstract = True


class Note(TimeStampedModel):
    title = models.TextField(verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    author = models.ForeignKey(
        'users.Profile', verbose_name="Author", on_delete=models.CASCADE, related_name="notes"
    )

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
