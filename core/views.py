from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Q
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from .models import User, Book, Category, Author, Loan
from .forms import RegisterForm, ProfileForm, BookForm, CategoryForm, AuthorForm
from .decorators import admin_required, normal_user_required


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return redirect("login")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Registration successful. Your Library ID is {user.library_id}.")
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    if request.user.is_library_admin:
        context = {
            "book_count": Book.objects.count(),
            "user_count": User.objects.filter(role=User.USER).count(),
            "active_count": Loan.objects.filter(status=Loan.ACTIVE).count(),
            "overdue_count": Loan.objects.filter(status=Loan.ACTIVE, due_at__lt=timezone.now()).count(),
            "recent_loans": Loan.objects.select_related("user", "book").all()[:7],
            "low_stock": Book.objects.filter(available_copies__lte=2)[:5],
        }
        return render(request, "admin/dashboard.html", context)
    loans = Loan.objects.filter(user=request.user).select_related("book")
    context = {
        "active_loans": loans.filter(status=Loan.ACTIVE),
        "history": loans[:6],
        "book_count": Book.objects.count(),
        "active_count": loans.filter(status=Loan.ACTIVE).count(),
    }
    return render(request, "user/dashboard.html", context)


def book_list(request):
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")
    books = Book.objects.select_related("author", "category").all()
    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__name__icontains=query) | Q(isbn__icontains=query))
    if category_id:
        books = books.filter(category_id=category_id)
    return render(request, "books/list.html", {
        "books": books, "categories": Category.objects.all(),
        "query": query, "selected_category": category_id
    })


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile has been updated.")
        return redirect("profile")
    return render(request, "registration/profile.html", {"form": form})


@login_required
def my_loans(request):
    loans = Loan.objects.filter(user=request.user).select_related("book", "issued_by")
    return render(request, "user/loans.html", {"loans": loans})


@admin_required
def user_search(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.filter(role=User.USER)
    if query:
        users = users.filter(Q(library_id__icontains=query) | Q(username__icontains=query) |
                             Q(first_name__icontains=query) | Q(last_name__icontains=query))
    return render(request, "admin/users.html", {"users": users, "query": query})


@admin_required
def user_detail(request, pk):
    member = get_object_or_404(User, pk=pk, role=User.USER)
    loans = Loan.objects.filter(user=member).select_related("book")
    return render(request, "admin/user_detail.html", {"member": member, "loans": loans})


@admin_required
def category_list(request):
    return render(request, "admin/categories.html", {"items": Category.objects.all()})


@admin_required
def category_create(request):
    return category_form(request, CategoryForm, "Category", "categories")


@admin_required
def category_edit(request, pk):
    return category_form(request, CategoryForm, "Category", "categories", get_object_or_404(Category, pk=pk))


@admin_required
def category_delete(request, pk):
    item = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        try:
            item.delete()
            messages.success(request, "Category deleted.")
        except Exception:
            messages.error(request, "This category is used by books. Reassign those books first.")
    return redirect("categories")


@admin_required
def author_list(request):
    return render(request, "admin/authors.html", {"items": Author.objects.all()})


@admin_required
def author_create(request):
    return category_form(request, AuthorForm, "Author", "authors")


@admin_required
def author_edit(request, pk):
    return category_form(request, AuthorForm, "Author", "authors", get_object_or_404(Author, pk=pk))


@admin_required
def author_delete(request, pk):
    item = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        try:
            item.delete()
            messages.success(request, "Author deleted.")
        except Exception:
            messages.error(request, "This author is linked to books. Reassign those books first.")
    return redirect("authors")


def category_form(request, form_class, label, redirect_name, instance=None):
    form = form_class(request.POST or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{label} saved successfully.")
        return redirect(redirect_name)
    return render(request, "admin/simple_form.html", {"form": form, "label": label})


@admin_required
def book_admin_list(request):
    query = request.GET.get("q", "").strip()
    books = Book.objects.select_related("author", "category")
    if query:
        books = books.filter(Q(title__icontains=query) | Q(isbn__icontains=query))
    return render(request, "admin/books.html", {"books": books, "query": query})


@admin_required
def book_create(request):
    form = BookForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Book added.")
        return redirect("manage_books")
    return render(request, "admin/book_form.html", {"form": form, "title": "Add book"})


@admin_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Book updated.")
        return redirect("manage_books")
    return render(request, "admin/book_form.html", {"form": form, "title": "Edit book"})


@admin_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        if book.loans.filter(status=Loan.ACTIVE).exists():
            messages.error(request, "Cannot delete a book while it is currently issued.")
        else:
            book.delete()
            messages.success(request, "Book deleted.")
    return redirect("manage_books")


@admin_required
def issue_book(request):
    if request.method == "POST":
        library_id = request.POST.get("library_id", "").strip()
        book_id = request.POST.get("book_id", "")
        member = get_object_or_404(User, library_id=library_id, role=User.USER)
        try:
            with transaction.atomic():
                book = Book.objects.select_for_update().get(pk=book_id)
                if book.available_copies < 1:
                    messages.error(request, "No copies of this book are currently available.")
                elif Loan.objects.filter(user=member, status=Loan.ACTIVE).count() >= 3:
                    messages.error(request, "This user already has the maximum of 3 active loans.")
                else:
                    book.available_copies -= 1
                    book.save(update_fields=["available_copies"])
                    Loan.objects.create(
                        user=member, book=book, issued_by=request.user,
                        due_at=timezone.now() + timedelta(days=14)
                    )
                    messages.success(request, f"'{book.title}' issued to {member.get_full_name() or member.username}.")
        except Book.DoesNotExist:
            messages.error(request, "Please select a valid book.")
        return redirect("issue_book")
    return render(request, "admin/issue.html", {
        "books": Book.objects.filter(available_copies__gt=0),
        "recent": Loan.objects.select_related("user", "book").filter(status=Loan.ACTIVE)[:8]
    })


@admin_required
def return_book(request, pk):
    loan = get_object_or_404(Loan.objects.select_related("book"), pk=pk)
    if request.method == "POST":
        with transaction.atomic():
            loan = Loan.objects.select_for_update().get(pk=pk)
            if loan.status == Loan.ACTIVE:
                book = Book.objects.select_for_update().get(pk=loan.book_id)
                loan.status = Loan.RETURNED
                loan.returned_at = timezone.now()
                loan.save(update_fields=["status", "returned_at"])
                book.available_copies = min(book.total_copies, book.available_copies + 1)
                book.save(update_fields=["available_copies"])
                messages.success(request, "Book return recorded successfully.")
            else:
                messages.warning(request, "This book has already been returned.")
    return redirect("issue_book")


class LibraryPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change.html"
    success_url = reverse_lazy("dashboard")
