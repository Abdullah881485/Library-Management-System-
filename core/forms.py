from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, Book, Category, Author


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)
    phone = forms.CharField(max_length=20, required=False)
    department = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "department"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.USER
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "department"]
        widgets = {"email": forms.EmailInput()}


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "isbn", "author", "category", "description",
                  "total_copies", "available_copies", "cover"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def clean(self):
        cleaned = super().clean()
        total = cleaned.get("total_copies")
        available = cleaned.get("available_copies")
        if total is not None and available is not None and available > total:
            self.add_error("available_copies", "Available copies cannot exceed total copies.")
        return cleaned


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "bio"]
