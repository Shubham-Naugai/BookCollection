from django.db import models
from datetime import date

# Create your models here.

class Book(models.Model):
    book_id = models.IntegerField(null = False, blank=False, primary_key=True, unique=True)
    book_title = models.CharField(max_length=225, null=False, blank=False)
    category = models.CharField(max_length=225, null=True, blank=True)
    author = models.CharField(max_length=225, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    publication_year = models.IntegerField()
    edition = models.edition = models.CharField(max_length=50, blank=True, null=True)
    upload_date = models.DateField(default=date.today)

    def __str__(self):
        return str(self.book_id)

class BookMedia(models.Model):
    book_id = models.OneToOneField(Book, on_delete=models.SET_NULL, null=True)
    book_cover_img = models.ImageField(null=True, blank=True)
    book_file = models.FileField(upload_to="pdf/", null=True, blank=True)

    def __str__(self):
        return str(self.book_id)

