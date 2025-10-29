from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'published_at', 'views')
    list_filter = ('status', 'category', 'author')
    search_fields = ('title', 'body', 'author__display_name')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-published_at',)

admin.site.register(Post, PostAdmin)
