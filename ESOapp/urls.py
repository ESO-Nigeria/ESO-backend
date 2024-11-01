# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ProgramViewSet, SocialLinkViewSet, RatingViewSet

router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profile')
router.register('programs', ProgramViewSet, basename='program')
router.register('social-links', SocialLinkViewSet, basename='sociallink')
router.register('ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]
