from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book-list'),
    path('book/<int:pk>/', views.book_detail, name='book-detail'),
    path('bookMedia/<int:pk>/', views.book_media, name='book-Media'),

    path('register/', views.registerUser, name="register"),
    # path('verify/', views.email_verification, name="verfication")

]
