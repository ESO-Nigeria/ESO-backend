import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from ESOapp.models import Profile, Program, SocialLink, Rating, AdminNotification

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        email='test@example.com',  # Add this line
        password='testpass123',
        organization_name='Test Org'
    )

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        username='admin',
        password='admin123',
        organization_name='Admin Org'
    )

@pytest.fixture
def profile(user):
    return Profile.objects.create(
        user=user,
        is_approved=False,
        state='CA',
        city='Test City'
    )

@pytest.fixture
def program(profile):
    return Program.objects.create(
        profile=profile,
        title='Test Program',
        is_approved=False,
        start_date='2024-01-01',
        end_date='2024-12-31'
    )
@pytest.fixture
def admin_notification(admin_user):
    return AdminNotification.objects.create(
        admin=admin_user,
        message="Test notification",
        notification_type="PROFILE_APPROVAL",
        is_read=False
    )
@pytest.mark.django_db
class TestProfileViewSet:
    def test_list_profiles_anonymous(self, api_client, profile):
        url = reverse('profile-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0  # No approved profiles

    def test_list_profiles_authenticated(self, api_client, user, profile):
        api_client.force_authenticate(user=user)
        url = reverse('profile-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1  # User can see their own profile

    def test_create_profile_authenticated(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('profile-list')
        data = {
            'state': 'NY',
            'city': 'New York'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
@pytest.mark.django_db
class TestProgramViewSet:
    def test_list_programs_anonymous(self, api_client, program):
        url = reverse('program-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0  # No approved programs

    def test_list_programs_authenticated(self, api_client, user, program):
        api_client.force_authenticate(user=user)
        url = reverse('program-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1  # User can see their own programs

    def test_create_program_authenticated(self, api_client, user, profile):
        api_client.force_authenticate(user=user)
        url = reverse('program-list')
        data = {
            'profile': profile.id,
            'title': 'New Program',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'description': 'Test program description',  # Add required field
            'program_type': 'TYPE1'  # Add required field
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
@pytest.mark.django_db
class TestSocialLinkViewSet:
    def test_create_social_link(self, api_client, user, profile):  # Add profile parameter
        api_client.force_authenticate(user=user)
        url = reverse('sociallink-list')
        data = {
            'platform': 'twitter',
            'url': 'https://twitter.com/test',
            'profile': profile.id  # Add required profile field
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
class TestRatingViewSet:
    def test_create_rating(self, api_client, user, profile):
        api_client.force_authenticate(user=user)
        url = reverse('rating-list')
        data = {
            'profile': profile.id,
            'score': 5,
            'comment': 'Great profile!'  # Add required field
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
class TestAdminNotificationViewSet:
    def test_list_notifications_admin(self, api_client, admin_user, admin_notification):
        api_client.force_authenticate(user=admin_user)
        url = reverse('adminnotification-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['message'] == "Test notification"

    def test_list_notifications_non_admin(self, api_client, user, admin_notification):
        api_client.force_authenticate(user=user)
        url = reverse('adminnotification-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_mark_notification_as_read(self, api_client, admin_user, admin_notification):
        api_client.force_authenticate(user=admin_user)
        url = reverse('adminnotification-detail', kwargs={'pk': admin_notification.pk})
        data = {'is_read': True}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_read'] == True