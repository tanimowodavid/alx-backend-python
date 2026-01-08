from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        Expects a list of user IDs as participants.
        """
        participant_ids = request.data.get("participants", [])

        conversation = Conversation.objects.create()
        conversation.participants.add(*participant_ids)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def send_message(self, request, pk=None):
        """
        Send a message to an existing conversation.
        """
        conversation = self.get_object()

        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=serializer.validated_data["message_body"],
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

