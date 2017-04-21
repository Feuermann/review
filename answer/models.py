from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Review(BaseModel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=128)
    text = models.TextField()

    def __str__(self):
        user = self.author if self.author else "Anon"
        return "{}'s review".format(user)


class Comment(BaseModel):
    author = models.ForeignKey(User)
    text = models.TextField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def __str__(self):
        return "{}'s comment".format(self.author.username)