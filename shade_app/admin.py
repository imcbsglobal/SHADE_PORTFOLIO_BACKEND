from django.contrib import admin
from .models import Visitor, Smile, OurClient, Ceremonial, Demonstration

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['created_at']

@admin.register(Smile)
class SmileAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(OurClient)
class OurClientAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Ceremonial)
class CeremonialAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Demonstration)
class DemonstrationAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']