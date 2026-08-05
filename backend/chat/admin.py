from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "title",
        "created_at",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "conversation",
        "role",
        "created_at",
    )