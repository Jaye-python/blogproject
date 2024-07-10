from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from blog.models import BlogPost, Category, Comment
from accounts.models import CustomUser

class BlogPostInline(admin.TabularInline):
    model = BlogPost
    extra = 0
    fields = ('title', 'content', 'created_at', 'category')
    readonly_fields = ('title', 'created_at', 'category')
    can_delete = False
    

class CustomUserAdmin(BaseUserAdmin):
    inlines = (BlogPostInline,)
    list_display = ('email', 'is_staff', 'is_active', 'get_blogpost_count')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    def get_blogpost_count(self, obj):
        return obj.blogpost_set.count()

    get_blogpost_count.short_description = 'Blog Posts'
    


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Comment)