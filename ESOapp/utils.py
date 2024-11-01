from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import AdminNotification
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status



def notify_admins(action, item, item_type):
    admin_users = get_user_model().objects.filter(is_staff=True)
    
    if item_type == "profile":
        subject = f'Profile {action}: {item.user.organization_name}'
        message = f'A profile has been {action}:\nOrganization: {item.user.organization_name}'
    else:  # program
        subject = f'Program {action}: {item.title}'
        message = f'A program has been {action}:\nTitle: {item.title}'
    
    # Send email to all admins
    for admin in admin_users:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [admin.email],
            fail_silently=True,
        )
    
    # Create dashboard notification
    AdminNotification.objects.create(
        title=subject,
        message=message
    )

def perform_create_with_notification(serializer, item_type, user=None):
    if user:
        instance = serializer.save(user=user)
    else:
        instance = serializer.save()
    notify_admins('created', instance, item_type)
    return instance

def perform_update_with_notification(serializer, item_type):
    instance = serializer.save()
    notify_admins('updated', instance, item_type)
    return instance



def handle_approval(instance, approved):

    instance.is_approved = approved
    instance.save()
    
    action_type = "approved" if approved else "rejected"
    notify_admins(action_type, instance, instance.__class__.__name__.lower())
    
    return {
        "message": f"{instance.__class__.__name__} has been {action_type}",
        "status": status.HTTP_200_OK
    }
    


def send_approval_email(user_email, model_type='profile'):

    subject = f'{model_type.title()} Approved'
    if model_type.lower() == 'profile':
        message = "Your profile has been approved. Welcome to our platform!"
    else:
        message = "Your program has been approved and is now visible on the platform!"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

def send_rejection_email(user_email, reason=None, model_type='profile'):

    subject = f'{model_type.title()} Rejected'
    default_reason = "Your submission did not meet our current requirements."
    message = f"Your {model_type} has been rejected.\nReason: {reason or default_reason}"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )