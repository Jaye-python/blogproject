from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from blog.forms import CommentForm, CreateBlogPostForm, CreateCategoryForm
from .models import BlogPost, Category
from django.db.models import Q
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect



 ####################### ANCHOR BLOG
class BlogPostListView(ListView):
    model = BlogPost
    context_object_name = 'blogposts'
    template_name = 'blog/blogposts.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        base_queryset = BlogPost.objects.all()
        search_query = self.request.GET.get('q', None)
        category = self.request.GET.get('category', None)

        if search_query:
            self.queryset = base_queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))
        elif category:
            self.queryset = base_queryset.filter(category__name__icontains=category)
        else:
            self.queryset = base_queryset
        return self.queryset

  
class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = CreateBlogPostForm
    template_name = 'blog/create_blog_post.html'
    success_url = reverse_lazy('blogposts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = CreateBlogPostForm
    template_name = 'blog/update_blog_post.html'
    success_url = reverse_lazy('blogposts')

    def dispatch(self, request, *args, **kwargs):
        blogpost = self.get_object()
        if blogpost.author != self.request.user:
            messages.error(self.request, 'You are not authorized to update this blog post.')
            return redirect('blogposts')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Blog Post updated successfully!')
        return response

class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blogposts')

    def dispatch(self, request, *args, **kwargs):
        blogpost = self.get_object()
        if blogpost.author != self.request.user:
            messages.error(self.request, 'You are not authorized to delete this blog post.')
            return redirect('blogposts')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, 'Blog Post deleted successfully!')
        return response


def blogpost_detail(request, pk):
    blogpost = get_object_or_404(BlogPost.objects.select_related('category', 'author'), pk=pk)
    comments = blogpost.comments.select_related('blogpost')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.blogpost = blogpost
            new_comment.save()
            return redirect('blogpost-detail', pk=blogpost.pk)
    else:
        comment_form = CommentForm()

    context = {
        'blogpost': blogpost,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/blogpost_detail.html', context)
   
   
 ####################### ANCHOR CATEGORY
    
class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'blog/categories.html'
    paginate_by = 5

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = 'blog/create_category.html'
    success_url = reverse_lazy('blogposts')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Category created successfully!')
        return response
    
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CreateCategoryForm
    template_name = 'blog/update_category.html'
    success_url = reverse_lazy('blogposts')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Category updated successfully!')
        return response


def load_categories(request):
    categories = Category.objects.all().values('id', 'name')
    return JsonResponse(list(categories), safe=False)