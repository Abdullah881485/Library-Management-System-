from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    ADMIN = "ADMIN"
    USER = "USER"
    ROLE_CHOICES = [(ADMIN, "Admin"), (USER, "User")]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)
    library_id = models.CharField(max_length=20, unique=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.library_id:
            # Generate a readable ID; retry if another account already uses it.
            import uuid
            self.library_id = f"LIB-{timezone.now():%y%m%d}-{uuid.uuid4().hex[:5].upper()}"
        super().save(*args, **kwargs)

    @property
    def is_library_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    def __str__(self):
        return f"{self.username} ({self.library_id})"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=30, unique=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="books")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="books")
    description = models.TextField(blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    cover = models.URLField(blank=True, help_text="Optional image URL for the book cover")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Loan(models.Model):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    STATUS_CHOICES = [(ACTIVE, "Issued"), (RETURNED, "Returned")]

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="loans")
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="loans")
    issued_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="issued_loans")
    issued_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        ordering = ["-issued_at"]

    def save(self, *args, **kwargs):
        if not self.due_at:
            self.due_at = self.issued_at + timedelta(days=14)
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        return self.status == self.ACTIVE and self.due_at < timezone.now()

    def __str__(self):
        return f"{self.book.title} → {self.user.library_id}"
