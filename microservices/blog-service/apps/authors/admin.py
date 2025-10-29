from django.contrib import admin
from .models import Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'email')
    search_fields = ('display_name', 'email')

admin.site.register(Author, AuthorAdmin)
