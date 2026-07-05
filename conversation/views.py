from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from item.models import Item

from .models import Conversation
from .serializers import ConversationMessageSerializer, ConversationSerializer


class InboxView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Conversation.objects.filter(members__in=[self.request.user.id])


class ConversationDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_conversation(self, request, pk):
        return get_object_or_404(
            Conversation.objects.filter(members__in=[request.user.id]), pk=pk
        )

    def get(self, request, pk):
        conversation = self.get_conversation(request, pk)
        return Response(ConversationSerializer(conversation).data)

    def post(self, request, pk):
        conversation = self.get_conversation(request, pk)
        serializer = ConversationMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(conversation=conversation, created_by=request.user)

        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class StartConversationView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, item_pk):
        item = get_object_or_404(Item, pk=item_pk)

        if item.created_by == request.user:
            return Response(
                {'detail': "You can't start a conversation about your own item."},
                status=status.HTTP_403_FORBIDDEN,
            )

        existing = Conversation.objects.filter(item=item).filter(members__in=[request.user.id]).first()

        if existing:
            return Response(ConversationSerializer(existing).data, status=status.HTTP_200_OK)

        message_serializer = ConversationMessageSerializer(data=request.data)
        message_serializer.is_valid(raise_exception=True)

        conversation = Conversation.objects.create(item=item)
        conversation.members.add(request.user, item.created_by)

        message_serializer.save(conversation=conversation, created_by=request.user)

        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)
