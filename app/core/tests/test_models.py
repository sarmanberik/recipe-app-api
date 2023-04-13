from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example', password='testpass123'):
    return get_user_model().objects.create_user(email, password)


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
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raise_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@local.local',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            'test@local.local',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Sample receipe description.',
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)
