from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # fields = ('text', 'review')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, source='comment_set', read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        # read_only = ('comments',)


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        write_only_fields = ('password',)