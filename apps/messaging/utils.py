from django.db.models import Max
from .models import Conversation, Message
from django.db.models import Q
from collections import OrderedDict


def get_user_conversations(user):
    """
    Returns all user converstions in most recent order
    """
    return (
        Conversation.objects.filter(participants=user)
        .annotate(last_message_time=Max("messages__sent_at"))
        .order_by("-last_message_time")
    )


def get_unique_participants(conversations, user):
    """
    Returns a list of unique  participants from each conversation excluding user
    """
    # List for all other participants in each conversation
    other_participants_list = []

    for conversation in conversations:
        # Exclude the current_user to get the other participant(s)
        other_participant = conversation.participants.exclude(id=user.id)
        # Add the other participant(s) to the list
        other_participants_list.extend(other_participant)

    # Remove duplicates from the list, keeping unique participants
    unique_participants = list(set(other_participants_list))

    return unique_participants


def get_conversation_message_history(user1, user2):
    """
    Retrieve conversation messages between two users
    """
    return Message.objects.filter(
        Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1)
    ).order_by("sent_at")


def get_recent_messages(current_user, unique_participants):
    """
    Returns a dictionary of the unique users and the last message between the current_user ordered by last message sent
    """
    unordered_dict = {}

    for participant in unique_participants:
        conversation = get_conversation_message_history(current_user, participant)

        # Fetch the last message in the conversation if it exists
        last_message = conversation.last() if conversation.exists() else None
        
        unordered_dict[participant] = last_message
    
    ordered_dict = OrderedDict(sorted(unordered_dict.items(), key=lambda x: x[1].sent_at if x[1] else None, reverse=True))

    return ordered_dict

# Create a read-status model