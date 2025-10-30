import uuid
from django.db import models
from apps.category.models import Category
from apps.authors.models import Author


class Post(models.Model):
    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=255)
    body = models.TextField()

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')

    status = models.CharField(max_length=10, choices=options, default='draft')

    published_at = models.DateTimeField(null=True, blank=True)
    views = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ('-published_at',)

    def __str__(self):
        return self.title