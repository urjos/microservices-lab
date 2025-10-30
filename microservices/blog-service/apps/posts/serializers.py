from rest_framework import serializers
from .models import Post
from apps.authors.models import Author
from apps.category.models import Category
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

class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = [
            'title', 'body', 'author', 'category', 'status'
        ]
        read_only_fields = ['slug', 'published_at', 'views'] # Estos se generarán automáticamente o se establecerán

    def create(self, validated_data):
        # Generamos el slug automáticamente a partir del título
        from slugify import slugify
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)