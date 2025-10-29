import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from slugify import slugify

from apps.category.models import Category
from apps.authors.models import Author
from apps.posts.models import Post

class Command(BaseCommand):
    help = 'Seeds the database with initial data for the blog'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to seed the database...")

        # Limpiar datos antiguos
        self.stdout.write("Cleaning old data...")
        Post.objects.all().delete()
        Category.objects.all().delete()
        Author.objects.all().delete()

        fake = Faker()

        # --- Crear Categorías ---
        self.stdout.write("Creating categories...")
        categories = []
        category_names = ['Technology', 'Software Development', 'Productivity', 'Business', 'Lifestyle']
        for name in category_names:
            category = Category.objects.create(name=name, slug=slugify(name))
            categories.append(category)
        self.stdout.write(self.style.SUCCESS(f"{len(categories)} categories created."))

        # --- Crear Autores ---
        self.stdout.write("Creating authors...")
        authors = []
        for _ in range(3):
            author = Author.objects.create(
                display_name=fake.name(),
                email=fake.unique.email()
            )
            authors.append(author)
        self.stdout.write(self.style.SUCCESS(f"{len(authors)} authors created."))

        # --- Crear Posts ---
        self.stdout.write("Creating posts...")
        posts = []
        for _ in range(30):
            title = fake.sentence(nb_words=6)
            status = random.choice(['published', 'draft'])
            post = Post.objects.create(
                title=title,
                slug=slugify(title),
                body=fake.paragraph(nb_sentences=20),
                author=random.choice(authors),
                category=random.choice(categories),
                status=status,
                published_at=timezone.now() if status == 'published' else None
            )
            posts.append(post)
        self.stdout.write(self.style.SUCCESS(f"{len(posts)} posts created."))
        self.stdout.write(self.style.SUCCESS("Database seeding complete!"))

