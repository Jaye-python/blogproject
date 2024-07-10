from django.test import TestCase, Client

from blog.forms import CommentForm, CreateBlogPostForm, CreateCategoryForm
from .models import BlogPost, Category, Comment
from django.urls import reverse
from django.contrib.auth import get_user_model


######ANCHOR TEST CATEGORY MODEL
class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Technology', description='Category for tech-related posts')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_description_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)

    def test_object_name_is_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = category.name
        self.assertEqual(expected_object_name, str(category))

    def test_ordering(self):
        categories = Category.objects.all()
        self.assertEqual(categories[0].name, 'Technology')


######ANCHOR TEST BLOG MODEL
class BlogPostModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='lagoslagos')
        category = Category.objects.create(name='Technology')
        BlogPost.objects.create(title='Sample Post', content='This is a sample post', category=category, author_id=self.user.id)

    def test_title_label(self):
        post = BlogPost.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_content_label(self):
        post = BlogPost.objects.get(id=1)
        field_label = post._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')

    def test_category_label(self):
        post = BlogPost.objects.get(id=1)
        field_label = post._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'category')

    def test_author_label(self):
        post = BlogPost.objects.get(id=1)
        field_label = post._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_created_at_label(self):
        post = BlogPost.objects.get(id=1)
        field_label = post._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_modified_at_label(self):
        post = BlogPost.objects.get(id=1)
        field_label = post._meta.get_field('modified_at').verbose_name
        self.assertEqual(field_label, 'modified at')

    def test_object_name_is_title(self):
        post = BlogPost.objects.get(id=1)
        expected_object_name = post.title
        self.assertEqual(expected_object_name, str(post))

    def test_ordering(self):
        posts = BlogPost.objects.all()
        self.assertEqual(posts[0].title, 'Sample Post')


######ANCHOR TEST COMMENT MODEL
class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='lagoslagos')
        category = Category.objects.create(name='Technology')
        blog_post = BlogPost.objects.create(title='Sample Post', content='This is a sample post', category=category, author_id=self.user.id)
        Comment.objects.create(blogpost=blog_post, comment='This is a test comment')

    def test_blogpost_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('blogpost').verbose_name
        self.assertEqual(field_label, 'blogpost')

    def test_comment_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('comment').verbose_name
        self.assertEqual(field_label, 'comment')

    def test_created_at_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_object_name(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = f'Comment on {comment.blogpost}'
        self.assertEqual(expected_object_name, str(comment))

############## ANCHOR TEST VIEWS

class BlogPostListViewTest(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='lagoslagos'
        )
        self.client = Client()
        self.client.login(email='testuser@example.com', password='lagoslagos')
        self.category = Category.objects.create(name='Test Category')
        self.blogpost1 = BlogPost.objects.create(
            title='Test Post 1',
            content='Content of Test Post 1',
            category=self.category,
            author=self.user,
        )
        self.blogpost2 = BlogPost.objects.create(
            title='Test Post 2',
            content='Content of Test Post 2',
            category=self.category,
            author=self.user,
        )
    
    def test_blogpost_list_view_with_search_query(self):
        url = reverse('blogposts')
        response = self.client.get(url, {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
    
    def test_blogpost_list_view_with_category_filter(self):
        url = reverse('blogposts')
        response = self.client.get(url, {'category': self.category.pk})
        self.assertEqual(response.status_code, 200)

class BlogPostCreateViewTest(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='lagoslagos'
        )
        self.client = Client()
        self.client.login(email='testuser@example.com', password='lagoslagos')
    
    def test_create_blogpost_view(self):
        url = reverse('create-blogpost')
        response = self.client.post(url, {
            'title': 'New Test Post',
            'content': 'Content of New Test Post',
        })
        self.assertEqual(response.status_code, 302)

class BlogPostUpdateViewTest(TestCase):
    
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            email='user1@example.com',
            password='lagoslagos1'
        )
        self.user2 = get_user_model().objects.create_user(
            email='user2@example.com',
            password='lagoslagos2'
        )
        self.client = Client()
        self.client.login(email='user1@example.com', password='lagoslagos1')
        self.blogpost = BlogPost.objects.create(
            title='Test Post',
            content='Content of Test Post',
            author=self.user1,
        )
    
    def test_update_blogpost_view_as_author(self):
        url = reverse('update-blogpost', kwargs={'pk': self.blogpost.pk})
        response = self.client.post(url, {
            'title': 'Updated Test Post',
            'content': 'Updated Content of Test Post',
        })
        self.assertEqual(response.status_code, 302)
    
    def test_update_blogpost_view_as_non_author(self):
        self.client.login(email='user2@example.com', password='lagoslagos2')
        url = reverse('update-blogpost', kwargs={'pk': self.blogpost.pk})
        response = self.client.post(url, {
            'title': 'Attempt to Update Test Post',
            'content': 'Attempt to Update Content of Test Post',
        })
        self.assertEqual(response.status_code, 302)

class BlogPostDeleteViewTest(TestCase):
    
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            email='user1@example.com',
            password='lagoslagos1'
        )
        self.user2 = get_user_model().objects.create_user(
            email='user2@example.com',
            password='lagoslagos2'
        )
        self.client = Client()
        self.client.login(email='user1@example.com', password='lagoslagos1')
        self.blogpost = BlogPost.objects.create(
            title='Test Post',
            content='Content of Test Post',
            author=self.user1,
        )
    
    def test_delete_blogpost_view_as_author(self):
        url = reverse('delete-blogpost', kwargs={'pk': self.blogpost.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
    
    def test_delete_blogpost_view_as_non_author(self):
        self.client.login(email='user2@example.com', password='lagoslagos2')
        url = reverse('delete-blogpost', kwargs={'pk': self.blogpost.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

class BlogPostDetailViewTest(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='lagoslagos'
        )
        self.client = Client()
        self.client.login(email='testuser@example.com', password='lagoslagos')
        self.category = Category.objects.create(name='Test Category')
        self.blogpost = BlogPost.objects.create(
            title='Test Post',
            content='Content of Test Post',
            category=self.category,
            author=self.user,
        )
    
    def test_create_comment_on_blogpost(self):
        url = reverse('blogpost-detail', kwargs={'pk': self.blogpost.pk})
        response = self.client.post(url, {
            'comment': 'This is a test comment.',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(comment='This is a test comment.').exists())


###### ANCHOR TEST FORMS

class CreateCategoryFormTest(TestCase):

    def test_create_category_form_valid(self):
        form_data = {
            'name': 'Test Category',
            'description': 'This is a test category.',
        }
        form = CreateCategoryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_category_form_invalid(self):
        form_data = {
            'name': '',  # Invalid because name is required
            'description': 'This is a test category.',
        }
        form = CreateCategoryForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        
class CreateBlogPostFormTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user( email='testuser@example.com', password='lagoslagos')
        self.category = Category.objects.create(name='Test Category', description='This is a test category.')

    def test_create_blogpost_form_valid(self):
        form_data = {
            'title': 'Test Blog Post',
            'content': 'This is a test blog post content.',
            'category': self.category.pk,
        }
        form = CreateBlogPostForm(data=form_data)
        form.instance.author = self.user
        self.assertTrue(form.is_valid())

    def test_create_blogpost_form_invalid(self):
        form_data = {
            'title': '',
            'content': 'This is a test blog post content.',
            'category': self.category.pk,
        }
        form = CreateBlogPostForm(data=form_data)
        form.instance.author = self.user
        self.assertFalse(form.is_valid())
        

class CommentFormTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user( email='testuser@example.com', password='lagoslagos')
        self.blogpost = BlogPost.objects.create(title='Test Blog Post', content='Test content', author_id=self.user.id)
        
    def test_comment_form_valid(self):
        form_data = {
            'comment': 'This is a test comment.',
        }
        form = CommentForm(data=form_data)
        form.instance.blogpost = self.blogpost
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        form_data = {
            'comment': '', 
        }
        form = CommentForm(data=form_data)
        form.instance.blogpost = self.blogpost
        self.assertFalse(form.is_valid())