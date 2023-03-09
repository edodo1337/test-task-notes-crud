from rest_framework import routers


from users.views import ProfileViewSet

router = routers.DefaultRouter()
router.register(r'', ProfileViewSet, basename='profile')
