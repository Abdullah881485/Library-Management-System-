from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Author, Book, Loan

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Library information", {"fields": ("role", "library_id", "phone", "department")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Library information", {"fields": ("role", "library_id", "phone", "department")}),)

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Loan)
