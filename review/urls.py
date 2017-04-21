"""review URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from answer.views import CommentViewSet, ReviewViewSet, UserViewSet, SignUp, SignIn
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'review', ReviewViewSet, 'review')
router.register(r'comment', CommentViewSet, 'comment')
router.register(r'users', UserViewSet, 'users')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^sign_up/$', SignUp.as_view(), name='sign_up'),
    url(r'^sign_in/$', SignIn.as_view(), name='sign_in'),
]
