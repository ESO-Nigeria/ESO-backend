# serializers.py

from rest_framework import serializers
from .models import Profile, Program, SocialLink, Rating
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from .models import CustomUser


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        # read_only_fields = ('id',)
        model = CustomUser
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserCreateSerializer(read_only=True)
    is_approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

class ProgramSerializer(serializers.ModelSerializer):
    is_approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = Program
        fields = '__all__'
        
class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['rated_by']
