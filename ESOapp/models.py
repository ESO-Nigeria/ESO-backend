# models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)  
    last_name = models.CharField(max_length=150)   
    organization_name = models.CharField(max_length=255)
    organization_type = models.CharField(
        max_length=3,
        choices=[
            ('FMS', 'Financial Management Services'),
            ('LS', 'Legal Services'),
            ('IRS', 'Investment-Readiness Services'),
            ('MC', 'Management Consulting'),
            ('ORS', 'Other Relevant Services'),
        ],
        blank=True,
        null=True
    )
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        verbose_name = "ESO's"  
        verbose_name_plural = "ESO's"  

    def __str__(self):
        return self.email

    


class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profile')
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company_email = models.EmailField(blank=True, null=True)
    company_phone = models.CharField(max_length=20, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.organization_name}"
    
class Rating(models.Model):
    rated_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    rated_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='ratings')  # Add this line
    rated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_ratings')
    rating = models.PositiveIntegerField()  # Assuming a 1-5 star rating system
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rated_user', 'rated_by')  # Ensure that a user can rate another user only once

    def __str__(self):
        return f"{self.rated_user.organization_name} rated by {self.rated_by.organization_name}"
    
    
class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('LinkedIn', 'LinkedIn'),
        ('Twitter', 'Twitter'),
        ('Facebook', 'Facebook'),
        ('YouTube', 'YouTube'),
    ]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField()

    def __str__(self):
        return f"{self.user.organization_name} - {self.platform}"


class Program(models.Model):
    profile = models.ForeignKey(Profile, related_name='programs', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    target_audience = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    funding = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

class AdminNotification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

