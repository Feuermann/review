import requests
from django.db.models import Prefetch
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from rest_framework import status, response
from rest_framework import viewsets, generics, permissions
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from oauth2_provider.models import Application

from answer.models import Review, Comment
from answer.serializers import ReviewSerializer, CommentSerializer, UserSerializer, SignUpSerializer
from answer.permisions import IsAuthenticatedOrCreate


class ReviewViewSet(viewsets.ModelViewSet):
    """Provides functionality to view, add, update and delete reviews,
    for list query, add serialized comment for each entry.
    """

    queryset = Review.objects.prefetch_related('comment_set')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]


class CommentViewSet(viewsets.ModelViewSet):
    """Provides functionality to view, add, update and delete comment"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]


class UserViewSet(viewsets.ModelViewSet):
    """Provides functionality to view, add, update and delete user"""

    queryset = User.objects.exclude(is_active=False)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def destroy(self, request, *args, **kwargs):
        if not User.objects.get(pk=kwargs.get('pk')).is_active:
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
    permission_classes = [IsAuthenticatedOrCreate, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = make_password(request.data.get('password'))
        serializer.save(password=password)
        message = "User has been created."
        return response.Response(message, status=status.HTTP_201_CREATED)


class SignIn(generics.CreateAPIView):
    """Class provide functionality for login user with username and password after Sign_Up.
    """
    permission_classes = [IsAuthenticatedOrCreate, ]

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        url = 'http://{}:{}/o/token/'.format(settings.SERVER_URL, settings.SERVER_PORT)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return response.Response({'detail': 'Credentials are wrong'}, status=status.HTTP_404_NOT_FOUND)

        app = Application.objects.filter(name='default', user=user).first()
        data = {
            'username': username,
            'password': password,
            'grant_type': 'password',
            'client_id': app.client_id
        }
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        resp = requests.post(url, data=data, headers=header)
        return response.Response(data=resp.json(), status=resp.status_code)


@receiver(post_save, sender=User)
def create_user_settings(sender, instance=None, created=False, **kwargs):
    """ For created user, creating Application instance for oauth2 model,
        use 'client_type = public' for authorization with client_id without client_secret,
        and 'grant_type = password' for password authenticate.
        Value for variable from oauth source code.
    """
    if created:
        app = Application()
        app.user = instance
        app.name = 'default'
        app.authorization_grant_type = 'password'
        app.client_type = 'public'
        app.save()
