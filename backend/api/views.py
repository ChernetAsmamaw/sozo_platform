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
    

class CategoryListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return api_models.Category.objects.all()
    

class PostCategoryListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = api_models.Category.objects.get(slug=category_slug)
        return api_models.Post.objects.filter(category=category, status='Active')


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


# Like posts 
class LikePostAPIView(APIView):

    # Tweaking the swagger documentation to add the request body
    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'post_id': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            )
    )

    def post(self, request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']

        user = api_models.User.objects.get(id=user_id)
        post = api_models.Post.objects.get(id=post_id)

        if user in post.like.all():
            post.like.remove(user)
            return Response({'message': 'Post Unliked'}, status=status.HTTP_200_OK)
        else:
            post.like.add(user)
            
            # create notification for the post owner
            api_models.Notification.objects.create(
                user=post.user,
                post=post,
                type='Like'
            )

            return Response({'message': 'Post Liked'}, status=status.HTTP_200_OK)
        

# Create a new comment for a post
class PostCommentAPIView(APIView):

    # Tweaking the swagger documentation to add the request body
    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'post_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'comment': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
    )

    def post(self, request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']
        comment = request.data['comment']

        post = api_models.Post.objects.get(id=post_id)

        api_models.Comment.objects.create(
            user_id=user_id,
            post=post,
            comment=comment
        )

        # create notification for the post owner
        api_models.Notification.objects.create(
            user=post.user,
            post=post,
            type='Comment'
        )

        return Response({'message': 'Comment Added'}, status=status.HTTP_200_OK)
    

# Create a bookmark for a post
class BookmarkPostAPIView(APIView):

    # Tweaking the swagger documentation to add the request body
    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'post_id': openapi.Schema(type=openapi.TYPE_INTEGER)
                }
            )
    )

    def post(self, request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']

        user = api_models.User.objects.get(id=user_id)
        post = api_models.Post.objects.get(id=post_id)

        # check if the user has already bookmarked the post
        bookmark = api_models.Bookmark.objects.filter(user=user, post=post).first()
        if bookmark:
            bookmark.delete()
            return Response({'message': 'Bookmark Removed'}, status=status.HTTP_200_OK)
        else:
            api_models.Bookmark.objects.create(
                user=user,
                post=post
            )        
            # create notification for the post owner
            api_models.Notification.objects.create(
                user=post.user,
                post=post,
                type='Bookmark'
            )

            return Response({'message': 'Bookmark Added'}, status=status.HTTP_200_OK)
        

# Create the dashboard for the user
class DashboardStats(generics.ListAPIView):
    serializer_class = api_serializer.AuthorSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # required the user id to be passed in the url
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)
        
        # get the total views, likes, posts and bookmarks for the user
        views = api_models.Post.objects.filter(user=user).aggregate(Sum('view'))['view__sum']
        likes = api_models.Post.objects.filter(user=user).aggregate(Sum('like'))['like__sum']
        posts = api_models.Post.objects.filter(user=user).count()
        bookmarks = api_models.Bookmark.objects.filter(post__user=user).count()

        return [{
            'views': views,
            'likes': likes,
            'posts': posts,
            'bookmarks': bookmarks
        }]
    
    # Override the default list method and send the serialized data in the response
    def list(self, request, *args, **kwargs):
        # call the get_queryset method above to get all the data
        queryset = self.get_queryset()
        # serialize the queryset data
        serializer = api_serializer.AuthorSerializer(queryset, many=True) # many=True because the queryset is a list of dictionaries more than one
        # return the serialized data in the response
        return Response(serializer.data) # data is the serialized data


# Create a list of posts in the dashboard
class DashBoardPostLists(generics.ListAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)
        return api_models.Post.objects.filter(user=user).order_by('-id')


# List the comments on the author's posts
class DashboardCommentLists(generics.ListAPIView):
    serializer_class = api_serializer.CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Multi author so no need to filter by user
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)
        return api_models.Comment.objects.filter(post__user=user).order_by('-id')
    

# List the notifications for the author
class DashboardNotificationLists(generics.ListAPIView):
    serializer_class = api_serializer.NotificationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Multi author so no need to filter by user
        user_id = self.kwargs['user_id']
        user = api_models.User.objects.get(id=user_id)
        return api_models.Notification.objects.filter(seen=False, user=user)


# Create a list of Notifications as read in the dashboard
class DashboardNotificationMarkRead(APIView):

    # Tweaking the swagger documentation to add the request body
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'notification_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            },
        ),
    )
    def post(self, request):
        notification_id = request.data['notification_id']
        notification = api_models.Notification.objects.get(id=notification_id)

        notification.seen = True
        notification.save()

        return Response({"message": "Notification Marked as Read"}, status=status.HTTP_200_OK)


# Allow the author to reply to the comments
class DashboardReplyCommentAPIView(APIView):

    # Tweaking the swagger documentation to add the request body
    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'comment_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'reply': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
    )

    def post(self, request):
        comment_id = request.data['comment_id']
        reply = request.data['reply']

        # Fetch the comment by the id and update the reply field
        comment = api_models.Comment.objects.get(id=comment_id)

        # Create a new comment object and save it
        api_models.Comment.objects.create(
            post=comment.post,
            user=comment.user,
            comment=reply,
            reply=comment
        )

        # It's already saved in the create method above but for clarity
        comment.save()


        return Response({'message': 'Comment Replied'}, status=status.HTTP_200_OK)


# Creating a new post
class DashboardCreatePostAPIView(APIView):

    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    # Tweaking the swagger documentation to add the request body
    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                    'image': openapi.Schema(type=openapi.TYPE_STRING),
                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                    'tags': openapi.Schema(type=openapi.TYPE_STRING),
                    'category': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'post_status': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
    )

    def post(self, request, *args, **kwargs):
        print(request.data)

        user_id = request.data.get('user_id')
        title = request.data.get('title')
        image = request.data.get('image')
        description = request.data.get('description')
        tags = request.data.get('tags')
        category_id = request.data.get('category')
        post_status = request.data.get('post_status')

        user = api_models.User.objects.get(id=user_id)
        category = api_models.Category.objects.get(id=category_id)

        api_models.Post.objects.create(
            user=user,
            title=title,
            image=image,
            tags=tags,
            description=description,
            category=category,
            status=post_status
        )

        return Response({'message': 'Post Created Successfully'}, status=status.HTTP_200_OK)
    

# Dashboard to update the post
class DashboardEditPostAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = api_serializer.PostSerializer
    permission_classes = [AllowAny]

    # Tweaking the swagger documentation to add the request body
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the post'),
                'image': openapi.Schema(type=openapi.TYPE_STRING, description='Image URL of the post'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the post'),
                'tags': openapi.Schema(type=openapi.TYPE_STRING, description='Tags associated with the post'),
                'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID of the post'),
                'post_status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the post')
            },
            required=['title']  # Adjust based on your requirements
        )
    )

    def get_object(self):
        user_id = self.kwargs['user_id']
        post_id = self.kwargs['post_id']
        user = api_models.User.objects.get(id=user_id)
        return api_models.Post.objects.get(user=user, id=post_id)

    def update(self, request, *args, **kwargs):
        post_instance = self.get_object()

        title = request.data.get('title')
        image = request.data.get('image')
        description = request.data.get('description')
        tags = request.data.get('tags')
        category_id = request.data.get('category')
        post_status = request.data.get('post_status')

        # Print the data to the console
        print(title)
        print(image)
        print(description)
        print(tags)
        print(category_id)
        print(post_status)
        print(post_instance)

        
        category = api_models.Category.objects.get(id=category_id)

        post_instance.title = title
        if image != 'undefined':
            post_instance.image = image
        post_instance.tags = tags
        post_instance.description = description
        post_instance.category = category
        post_instance.status = post_status
        
        post_instance.save()

        return Response({'message': 'Post Updated Successfully'}, status=status.HTTP_200_OK)
