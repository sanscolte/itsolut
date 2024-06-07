from django.contrib import admin

from api.models import Author, Advt


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = "id", "name"
    list_display_links = ("name",)


@admin.register(Advt)
class AuthorAdmin(admin.ModelAdmin):
    list_display = "id", "title", "author", "views", "position"
    list_display_links = ("title",)
    ordering = ("position",)
