from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from members.views import MemberViewSet
from music.views import ArtistViewSet, AlbumViewSet, SongViewSet, ScrobbleViewSet
from updates.views import UpdateViewSet

router = DefaultRouter()
router.register(r"members", MemberViewSet)
router.register(r"artists", ArtistViewSet)
router.register(r"albums", AlbumViewSet)
router.register(r"songs", SongViewSet)
router.register(r"scrobbles", ScrobbleViewSet)
router.register(r"updates", UpdateViewSet)

urlpatterns = [
    path('fux/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', views.obtain_auth_token),
] + static('/', document_root=settings.MEDIA_ROOT)
