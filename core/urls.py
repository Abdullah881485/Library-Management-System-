from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("books/", views.book_list, name="book_list"),
    path("profile/", views.profile, name="profile"),
    path("my-loans/", views.my_loans, name="my_loans"),
    path("password/change/", views.LibraryPasswordChangeView.as_view(), name="password_change"),
    path("password/reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset.html",
        email_template_name="registration/password_reset_email.html",
        success_url="/password/reset/done/"
    ), name="password_reset"),
    path("password/reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"
    ), name="password_reset_done"),
    path("password/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html",
        success_url="/password/reset/complete/"
    ), name="password_reset_confirm"),
    path("password/reset/complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ), name="password_reset_complete"),

    path("admin-panel/users/", views.user_search, name="users"),
    path("admin-panel/users/<int:pk>/", views.user_detail, name="user_detail"),
    path("admin-panel/categories/", views.category_list, name="categories"),
    path("admin-panel/categories/add/", views.category_create, name="category_add"),
    path("admin-panel/categories/<int:pk>/edit/", views.category_edit, name="category_edit"),
    path("admin-panel/categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("admin-panel/authors/", views.author_list, name="authors"),
    path("admin-panel/authors/add/", views.author_create, name="author_add"),
    path("admin-panel/authors/<int:pk>/edit/", views.author_edit, name="author_edit"),
    path("admin-panel/authors/<int:pk>/delete/", views.author_delete, name="author_delete"),
    path("admin-panel/books/", views.book_admin_list, name="manage_books"),
    path("admin-panel/books/add/", views.book_create, name="book_add"),
    path("admin-panel/books/<int:pk>/edit/", views.book_edit, name="book_edit"),
    path("admin-panel/books/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("admin-panel/issue/", views.issue_book, name="issue_book"),
    path("admin-panel/return/<int:pk>/", views.return_book, name="return_book"),
]
