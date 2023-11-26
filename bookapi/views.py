from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Book, BookMedia
from .serializers import BookSerializer, UserSerializerWithToken, BookMediaSerializer

from .utils import send_email_to_client

# Create your views here.


# def email_verification(request):
#     send_email_to_client()
#     return Response({'email': 'verified'}, status=status.HTTP_201_CREATED)


class BookPagination(PageNumberPagination):
    page_size = 3  # Set the number of books per page
    page_size_query_param = 'page_size'
    max_page_size = 30


@api_view(['GET', 'POST'])
def book_list(request):
    paginator = BookPagination()

    if request.method == 'GET':
        books = Book.objects.all()

        # Advanced Filtering
        title = request.query_params.get('title', None)
        author = request.query_params.get('author', None)
        category = request.query_params.get('category', None)

        if title:
            books = books.filter(book_title__icontains=title)
        if author:
            books = books.filter(author__icontains=author)
        if category:
            books = books.filter(category__icontains=category)

        # Sorting
        ordering = request.query_params.get('ordering', None)
        if ordering:
            books = books.order_by(ordering)
        
        # Pagination
        result_page = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
        
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            first_name = data['name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password'])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['GET', 'POST'])
def book_media(request, pk):
    if request.method == 'POST':
        image_file = request.data['image_file']
        pdf_file = request.data['pdf_file']

        # Validate file size
        if image_file.size > 2 * 1024 * 1024:  # 2 kb limit
            return Response({'error': 'Image size exceeds the limit (2 MB)'}, status=status.HTTP_400_BAD_REQUEST)
        if pdf_file.size > 4 * 1024 * 1024:  # 2 MB limit
            return Response({'error': 'PDF size exceeds the limit (4 MB)'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'file/pdf']  # Adjust allowed types
        if image_file.content_type not in allowed_types:
            return Response({'error': 'Invalid file type'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the file to the book record
        serializer = BookMediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)