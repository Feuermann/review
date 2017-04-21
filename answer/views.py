from django.shortcuts import render
from django.db.models import Prefetch
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, permissions
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer, UserSerializer, SignUpSerializer
from answer.permisions import IsAuthenticatedOrCreate


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.prefetch_related('comment_set')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    authentication_classes = (IsAuthenticatedOrCreate, )
