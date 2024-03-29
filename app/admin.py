from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, NewsletterSubscription, PressReleaseSubmission
from .forms import CustomUserCreationForm, CustomUserChangeForm, SubscriptionForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', "num_credits", "date_joined", "last_login")}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', "num_credits", "date_joined", "last_login")}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

@admin.register(NewsletterSubscription)
class NewsletterAdmin(admin.ModelAdmin):
    add_form = SubscriptionForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email',)
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(PressReleaseSubmission)