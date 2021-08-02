from django.test import TestCase
from django.contrib.auth import get_user_model


class UserAccountTest(TestCase):

    def test_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', 'username', 'password')
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.username, 'username')
        self.assertTrue(super_user.is_admin)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), "username")

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', username='username1', password='password')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@super.com', username='', password='password')

    def test_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'username', 'password')
        self.assertEqual(user.email, 'testuser@user.com')
        self.assertEqual(user.username, 'username')
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='', username='username1', password='password')

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='testuser@super.com', username='', password='password')

    def test_staff(self):
        db = get_user_model()
        user = db.objects.create_staff_user(
            'testuser@user.com', 'username', 'password')
        self.assertEqual(user.email, 'testuser@user.com')
        self.assertEqual(user.username, 'username')
        self.assertFalse(user.is_admin)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='', username='username1', password='password')

        with self.assertRaises(ValueError):
            db.objects.create_user(
                email='testuser@super.com', username='', password='password')

    def test_get_user_email(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'username', 'password')
        expected_email = "testuser@user.com"
        self.assertEqual(expected_email, user.get_email())

    def test_get_user_is_admin_status(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'username', 'password')
        self.assertFalse(user._is_admin)

    def test_get_user_is_staff_status(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'username', 'password')
        self.assertFalse(user._is_staff)

    def test_get_user_is_active_status(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'username', 'password')
        self.assertFalse(user._is_active)

    def test_user_has_perm(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'username', 'password')
        expected_perm = True
        self.assertEqual(expected_perm, user.has_perm('user.delete_user'))

    def test_user_has_model_perm(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'username', 'password')
        expected_perm = True
        self.assertEqual(expected_perm, user.has_module_perms('user'))

    def test_get_user_profile_image_path(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', 'username', 'password')
        expected_path = 'media/images/profile_pics/default_icon.png'
        self.assertEqual(expected_path, user.get_profile_image_path())
