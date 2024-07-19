from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.db.models import Sum
# Restframework
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import datetime

# Others
import json
import random

# Custom Imports
from api import serializer as api_serializer
from api import models as api_models



# generate the token for the user
# This class is inherited from TokenObtainPairView which is a class based view in Django Rest Framework
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer


# register the user
# This class is inherited from generics.GenericAPIView which is a class based view in Django Rest Framework
class RegisterView(generics.GenericAPIView):
    queryset = api_models.User.objects.all()
    serializer_class = api_serializer.RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = api_models.Profile.objects.all()
    serializer_class = api_serializer.ProfileSerializer
    permission_classes = [AllowAny]

    # override the default get_object method to get the current user's profile
    # insted of the profile id the user id is passed in the url like /api/profile/<user_id>/ insted of /<profile_id>/
    def get_object(self):
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)
        profile = api_models.Profile.objects.get(user=user)
        return profile
    

class CatagoryListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return api_models.Category.objects.all()
    

class PostCatagoryListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        catagory_slug = self.kwargs['catagory_slug']
        catagory = api_models.Catagory.objects.get(slug=catagory_slug)
        return api_models.Post.objects.filter(catagory=catagory, status='Active')


# use list api view to get the list of all the posts
class PostListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return api_models.Post.objects.filter(status='Active')
    

# use retrieve api view to get the detail of a single post
class PostDetailAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs['slug']
        post = api_models.Post.objects.get(slug=slug, status='Active')
        post.views += 1
        post.save()
        return post
