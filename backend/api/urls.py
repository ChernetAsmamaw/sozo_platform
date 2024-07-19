from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from api import views as api_views

urlpatterns = [
    path('user/token/', api_views.MyTokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/register/', api_views.RegisterView.as_view()),
    path('user/profile/<int:user_id>/', api_views.ProfileView.as_view()),

    # Post endpoints
    path('post/catagory/list/', api_views.CatagoryListAPIView.as_view()),
    path('post/catagory/posts/<slug:catagory_slug>/', api_views.PostCatagoryListAPIView.as_view()),
    path('post/lists/', api_views.PostListAPIView.as_view()),
    path('post/detail/<slug:slug>/', api_views.PostDetailAPIView.as_view()),
]
