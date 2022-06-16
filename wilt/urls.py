from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from members.views import MemberViewSet
from music.views import ArtistViewSet, AlbumViewSet, SongViewSet

router = DefaultRouter()
router.register(r"members", MemberViewSet)
router.register(r"artists", ArtistViewSet)
router.register(r"albums", AlbumViewSet)
router.register(r"songs", SongViewSet)

urlpatterns = [
    path('pusherman/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
