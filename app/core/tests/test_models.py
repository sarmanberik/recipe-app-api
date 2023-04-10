from django.test import TestCase
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'test@local.local'
        password = 'P@ssw0rd123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_email_normalize(self):
        sample_emails = [
            ['test1.@LOCAL.LOCAL', 'test1.@local.local'],
            ['Test2.@Local.local', 'Test2.@local.local'],
            ['TEST3.@LOCAL.LOCAL', 'TEST3.@local.local'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'P@ssw0rd')
            self.assertEqual(user.email, expected )

    def test_new_user_without_email_raise_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test')