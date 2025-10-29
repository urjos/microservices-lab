from rest_framework import serializers
from .models import Post
from apps.authors.models import Author
from apps.category.serializers import CategorySerializer


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'display_name']


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'excerpt', 'author', 'category', 'published_at']

    def get_excerpt(self, obj):
        return obj.body[:150] + '...' if len(obj.body) > 150 else obj.body


class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'body',
            'author', 'category',
            'status', 'published_at', 'views'
        ]