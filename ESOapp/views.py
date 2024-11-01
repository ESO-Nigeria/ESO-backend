# views.py

from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated, BasePermission
from rest_framework import viewsets
from .models import Profile, Program
from .serializers import ProfileSerializer, ProgramSerializer
from .models import SocialLink, Rating
from .serializers import SocialLinkSerializer, RatingSerializer
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .utils import perform_create_with_notification, perform_update_with_notification


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    
class IsOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for approved items
        if request.method in ['GET', 'HEAD', 'OPTIONS'] and getattr(obj, 'is_approved', False):
            return True
            
        # Allow admin users
        if request.user.is_staff:
            return True
            
        if isinstance(obj, Program):
            return obj.profile.user == request.user
        return obj.user == request.user

    def has_permission(self, request, view):
        # Allow read-only access for all users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
            
        # For write operations, require authentication
        return request.user.is_authenticated


class ProfileViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        permission_classes = [IsOwnerOrAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.all().order_by('user__organization_name')
        elif self.request.user.is_authenticated:
            # Return approved items + user's own items
            return Profile.objects.filter(
                user=self.request.user
            ).order_by('user__organization_name')
        # For anonymous users, return only approved items
        return Profile.objects.filter(
            is_approved=True
        ).order_by('user__organization_name')
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return perform_create_with_notification(serializer, 'profile')

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        return perform_update_with_notification(serializer, 'profile')
    serializer_class = ProfileSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [OrderingFilter]
    filterset_fields = ["state","city"]
    ordering_fields = ["user__organization_type"]
    ordering = ["user__organization_name",]
    pagination_class = CustomPageNumberPagination



class ProgramViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        permission_classes = [IsOwnerOrAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Program.objects.all()
        elif self.request.user.is_authenticated:
            # Return approved items + user's own items
            return Program.objects.filter(
                profile__user=self.request.user
            )
        # For anonymous users, return only approved items
        return Program.objects.filter(is_approved=True)
    def perform_create(self, serializer):
        return perform_create_with_notification(serializer, 'program')

    def perform_update(self, serializer):
        return perform_update_with_notification(serializer, 'program')
    serializer_class = ProgramSerializer
    filter_backends = [OrderingFilter]
    filterset_fields = ["title"]
    ordering_fields = ["start_date", "end_date"]
    ordering = ["start_date","end_date"]
    pagination_class = CustomPageNumberPagination

class SocialLinkViewSet(viewsets.ModelViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(rated_by=self.request.user) 
