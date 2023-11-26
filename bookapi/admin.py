from django.contrib import admin
from .models import Book, BookMedia

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book_title')
admin.site.register(Book, BookAdmin)


class BookMediaAdmin(admin.ModelAdmin):
    list_display = ('book_id',)
admin.site.register(BookMedia, BookMediaAdmin)
