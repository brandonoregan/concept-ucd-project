from django.shortcuts import render
from .forms import CreateUser
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from apps.profiles.models import Profile
from apps.messaging.models import Message, Conversation
from .models import CustomUser


def welcome(request):
    return render(request, "users/welcome.html")


class LoginUser(SuccessMessageMixin, LoginView):
    template_name = "users/login_user.html"
    success_url = reverse_lazy("post_home")
    success_message = "You were successfully logged in."


class LogoutUser(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy("welcome")

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(self.request, ("You were successfully logged out."))
        return response


class RegisterUser(SuccessMessageMixin, CreateView):
    template_name = (
        "users/register_user.html"
    )
    form_class = CreateUser
    success_message = (
        "Your profile was created successfully. " "Please login to proceed."
    )
    success_url = reverse_lazy("login_user")

    # Login registered user on correct form validation
    def form_valid(self, form):
        # Save the user instance and get the user object
        user = form.save()

        # Create a Profile instance linked to the user
        Profile.objects.create(user=user)

        # Log in the user
        login(self.request, user)

        # Fetch the admin Custom User Object
        admin = CustomUser.objects.get(username="admin")

        # Create or retrieve conversation between admin and the new user
        conversation = (
            Conversation.objects.filter(participants=user)
            .filter(participants=admin)
            .first()
        )
        
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(user, admin)

        welcome_text = (
            "Welcome to your inbox! Use the search bar to find people to connect with, "
            "or even chat to me! "
            "I might reply...eventually."
        )

        # Create a welcome message from admin to the newly registered user
        message = Message.objects.create(
            sender=admin,
            receiver=user,
            text=welcome_text,
            conversation=conversation,
        )

        # Update the last_message timestamp of the conversation
        conversation.last_message = message.sent_at
        conversation.save()

        return super().form_valid(form)
