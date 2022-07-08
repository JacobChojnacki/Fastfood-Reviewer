from django.contrib import admin
from .models import Post, Comment, ProductReview
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish')
    list_filter = ('author', 'publish')
    search_field = ('title', 'body')
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'publish'
    ordering = ('author', "publish")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('email', 'post', 'created')
    list_filter = ('email', 'created', 'updated')
    search_fields = ('email','body')
    
admin.site.register(ProductReview)
