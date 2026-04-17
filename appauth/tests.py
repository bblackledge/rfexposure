from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from appauth.adapters import AccountAdapter


class AccountAdapterTests(TestCase):
    def setUp(self):
        self.request = RequestFactory().get("/")
        SessionMiddleware(lambda request: None).process_request(self.request)
        self.request.session.save()
        self.request._messages = FallbackStorage(self.request)
        self.adapter = AccountAdapter()

    def test_logged_in_message_is_suppressed(self):
        self.adapter.add_message(
            self.request,
            messages.SUCCESS,
            "account/messages/logged_in.txt",
            {"user": object()},
        )

        self.assertEqual(list(get_messages(self.request)), [])

    def test_logged_out_message_is_suppressed(self):
        self.adapter.add_message(
            self.request,
            messages.SUCCESS,
            "account/messages/logged_out.txt",
        )

        self.assertEqual(list(get_messages(self.request)), [])

    def test_other_messages_still_render(self):
        self.adapter.add_message(
            self.request,
            messages.INFO,
            message="Welcome back",
        )

        stored_messages = list(get_messages(self.request))
        self.assertEqual(len(stored_messages), 1)
        self.assertEqual(stored_messages[0].message, "Welcome back")
