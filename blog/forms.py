from django import forms
from .models import BlogPost, Category, Comment


class CreateCategoryForm(forms.ModelForm):        
    class Meta:
        model = Category
        fields = ['name', 'description']

class CreateBlogPostForm(forms.ModelForm):
        
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category']
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
