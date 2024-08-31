from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api import views as api_views

urlpatterns = [
    # User endpoints
    path('user/token/', api_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/register/', api_views.RegisterView.as_view()),
    path('user/profile/<int:user_id>/', api_views.ProfileView.as_view()),

    # Post endpoints
    path('post/category/list/', api_views.CategoryListAPIView.as_view()),
    path('post/category/posts/<slug:category_slug>/', api_views.PostCategoryListAPIView.as_view()),
    path('post/lists/', api_views.PostListAPIView.as_view()),
    path('post/detail/<slug:slug>/', api_views.PostDetailAPIView.as_view()),
    path('post/like-post/', api_views.LikePostAPIView.as_view()),
    path('post/comment-post/', api_views.PostCommentAPIView.as_view()),
    path('post/bookmark-post/', api_views.BookmarkPostAPIView.as_view()),
    
    # Author endpoints
    path('author/dashboard/stats/<user_id>/', api_views.DashboardStats.as_view()),
    path('author/dashboard/list-post/<user_id>', api_views.DashBoardPostLists.as_view()),
    path('author/dashboard/comment-list/<user_id>/', api_views.DashboardCommentLists.as_view()),
    path('author/dashboard/notification-list/<user_id>/', api_views.DashboardNotificationLists.as_view()),
    path('author/dashboard/comment-reply/', api_views.DashboardReplyCommentAPIView.as_view()),
    path('author/dashboard/notification-mark-as-read/', api_views.DashboardNotificationMarkRead.as_view()),
    path('author/dashboard/create-post/', api_views.DashboardCreatePostAPIView.as_view()),
    path('author/dashboard/edit-post/<user_id>/<post_id>/', api_views.DashboardEditPostAPIView.as_view()),
]