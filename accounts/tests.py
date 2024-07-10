from django.test import TestCase

from accounts.forms import SignupForm
from blog.models import BlogPost, Category
from .models import CustomUser
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

####### ANCHOR: TEST MODELS ################
class UserManagerTests(TestCase):

    def test_create_user(self):
        email = 'testuser@example.com'
        password = 'testpassword'
        user = CustomUser.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', password='testpassword')

    def test_create_superuser(self):
        email = 'admin@example.com'
        password = 'adminpassword'
        user = CustomUser.objects.create_superuser(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_without_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(email='', password='adminpassword')


####### ANCHOR: TEST VIEWS ################

class UserSignupTest(TestCase):
    def test_signup_page(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_user_signup(self):
        response = self.client.post(reverse('signup'), {
            'email': 'testuser@example.com',
            'password1': 'lagoslagos',
            'password2': 'lagoslagos'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blogposts'))
        user = get_user_model().objects.get(email='testuser@example.com')
        self.assertTrue(user)

class UserLoginTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='lagoslagos')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser@example.com',
            'password': 'lagoslagos'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blogposts'))



class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='lagoslagos')
        self.client.login(username='testuser@example.com', password='lagoslagos')

    def test_profile_view(self):
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_profile.html')
        self.assertEqual(response.context['blogposts'].count(), 0)
        
        category = Category.objects.create(name='Test Category')
        BlogPost.objects.create(title='Test Post', content='Test Content', author=self.user, category=category)
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.context['blogposts'].count(), 1)


class ProfileUpdateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='lagoslagos')
        self.client.login(username='testuser@example.com', password='lagoslagos')

    def test_profile_update(self):

        response = self.client.post(reverse('profile-update'), {
            'first_name': 'Updated',
            
        })
        if response.status_code != 302:
            print(response.context['form'].errors)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blogposts'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')


########## ANCHOR TEST FORMS

User = get_user_model()

class SignupFormTest(TestCase):

    def test_signup_form_valid(self):
        form_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'password1': 'lagoslagos',
            'password2': 'lagoslagos',
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid_email(self):
        User.objects.create_user(email='testuser@example.com', password='lagoslagos')

        form_data = {
            'email': 'testuser@example.com',  # Duplicate email
            'first_name': 'Test',
            'password1': 'lagoslagos',
            'password2': 'lagoslagos',
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_signup_form_password_mismatch(self):
        form_data = {
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'password1': 'lagoslagos',
            'password2': 'password456',
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
