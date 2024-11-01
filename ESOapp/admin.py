# admin.py

from django.contrib import admin
from .models import Profile, Program, SocialLink, Rating, CustomUser, AdminNotification
from django.contrib import messages
from .utils import send_approval_email, send_rejection_email
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.safestring import mark_safe

admin.site.unregister(Group)

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1  # Number of empty forms to display for adding new links

class RatingInline(admin.TabularInline):
    model = Rating  # Use rated_user to link ratings to users
    extra = 1

class ProgramInline(admin.TabularInline):
    model = Program
    extra = 1

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    @admin.action(description='Approve selected profiles')
    def approve_profiles(self, request, queryset):
        count = 0
        for profile in queryset:
            profile.is_approved = True
            profile.save()
            send_approval_email(profile.user.email, 'profile')
            count += 1
        self.message_user(request, f"{count} profiles were approved and users were notified.")

    @admin.action(description='Reject selected profiles with reason')
    def reject_profiles(self, request, queryset):
        reason = request.POST.get('rejection_reason')
        count = 0
        for profile in queryset:
            profile.is_approved = False
            profile.save()
            send_rejection_email(profile.user.email, reason, 'profile')
            count += 1
        self.message_user(request, f"{count} profiles were rejected and users were notified.")

    list_display = ('user', 'is_approved', 'needs_review')
    list_filter = ('is_approved',)
    actions = [approve_profiles, reject_profiles]
    inlines = [SocialLinkInline, RatingInline, ProgramInline]

    def needs_review(self, obj):
        return not obj.is_approved
    needs_review.boolean = True
    needs_review.short_description = 'Needs Review'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs
        
        pending_count = qs.filter(is_approved=False).count()
        if pending_count > 0:
            messages.warning(request, f'{pending_count} profile(s) waiting for approval')
        return qs 



@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    def approve_programs(self, request, queryset):
        count = 0
        for program in queryset:
            program.is_approved = True
            program.save()
            send_approval_email(program.user.email, 'program')
            count += 1
        self.message_user(request, f"{count} programs were approved and owners were notified.")

    @admin.action(description='Reject selected programs with reason')
    def reject_programs(self, request, queryset):
        reason = request.POST.get('rejection_reason')
        count = 0
        for program in queryset:
            program.is_approved = False
            program.save()
            send_rejection_email(program.user.email, reason, 'program')
            count += 1
        self.message_user(request, f"{count} programs were rejected and owners were notified.")
    list_display = ('title', 'is_approved', 'needs_review')
    list_filter = ('is_approved',)
    actions = [approve_programs, reject_programs]

    def needs_review(self, obj):
        return not obj.is_approved
    needs_review.boolean = True
    needs_review.short_description = 'Needs Review'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs
            
        pending_count = qs.filter(is_approved=False).count()
        if pending_count > 0:
            messages.warning(request, f'{pending_count} program(s) waiting for approval')
        return qs
    
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')
    
    
    fieldsets = (
        (None, {'fields': ( 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'message')
    ordering = ('-created_at',)
    list_per_page = 10
    
class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        # Get pending counts
        pending_profiles = Profile.objects.filter(is_approved=False).count()
        pending_programs = Program.objects.filter(is_approved=False).count()
        
        if pending_profiles > 0:
            profile_link = f'<a href="{reverse("admin:ESOapp_profile_changelist")}?is_approved__exact=0">Click here to view</a>'
            messages.warning(request, mark_safe(f'{pending_profiles} profile(s) waiting for approval. {profile_link}'))
        
        if pending_programs > 0:
            program_link = f'<a href="{reverse("admin:ESOapp_program_changelist")}?is_approved__exact=0">Click here to view</a>'
            messages.warning(request, mark_safe(f'{pending_programs} program(s) waiting for approval. {program_link}'))
            
        return super().index(request, extra_context)
    
admin.site = CustomAdminSite()
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(AdminNotification, AdminNotificationAdmin)