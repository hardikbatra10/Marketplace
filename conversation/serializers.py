from rest_framework import serializers

from item.serializers import ItemSerializer

from .models import Conversation, ConversationMessage


class ConversationMessageSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = ('id', 'conversation', 'content', 'created_by', 'created_at')
        read_only_fields = ('conversation', 'created_by', 'created_at')


class ConversationSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    members = serializers.StringRelatedField(many=True, read_only=True)
    messages = ConversationMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'item', 'members', 'messages', 'created_at', 'modified_at')
