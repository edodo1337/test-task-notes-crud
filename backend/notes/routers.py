from rest_framework import routers

from notes.views import NotesViewSet

router = routers.DefaultRouter()
router.register(r'notes', NotesViewSet)
