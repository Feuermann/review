from django.shortcuts import render
from django.db.models import Prefetch
from rest_framework import status, response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, generics, permissions
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

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
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.exclude(is_active=False)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def destroy(self, request, *args, **kwargs):
        if not User.objects.get(pk=kwargs.get('pk')).is_active :
            message = {'detail': 'User has been deleted.'}
            return response.Response(message, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        if self.request.user == instance:
            message = {'detail': "You can't remove himself"}
            return response.Response(message, status=status.HTTP_400_BAD_REQUEST)
        instance.is_active = False
        instance.save(update_fields=['is_active', ])
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    authentication_classes = (IsAuthenticatedOrCreate, )

