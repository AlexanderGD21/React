from datetime import timedelta

from django.test import SimpleTestCase
from django.utils import timezone

from .models import User
from .views import code_is_valid, generate_verification_code


class VerificationCodeTests(SimpleTestCase):
    def test_generates_a_six_digit_code(self):
        code = generate_verification_code()

        self.assertRegex(code, r'^\d{6}$')

    def test_accepts_an_unexpired_matching_code(self):
        user = User(
            verification_code='123456',
            verification_code_expires_at=timezone.now() + timedelta(minutes=1),
        )

        self.assertTrue(code_is_valid(user, '123456'))

    def test_rejects_an_expired_code(self):
        user = User(
            verification_code='123456',
            verification_code_expires_at=timezone.now() - timedelta(seconds=1),
        )

        self.assertFalse(code_is_valid(user, '123456'))
