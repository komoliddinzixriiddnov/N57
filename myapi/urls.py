from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MovieViewSet, ActorViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'actors', ActorViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path

from . import views
from .views import RegisterAPIView, VerifyOTPAPIView, ProfileAPIView, PhoneAPIView, CommentDetail, CommentListApiView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('send-otp/', PhoneAPIView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('me/', ProfileAPIView.as_view(), name='user_profile'),

    path("", views.MovieList.as_view(), name="movie_list"),
    path("<int:pk>/", views.MovieDetail.as_view(), name="movie_detail"),

    path("actor/", views.ActorList.as_view(), name="actor_list"),
    path("actor/<int:pk>/", views.ActorDetail.as_view(), name="actor_detail"),

    path('<int:movie_id>/comments/', CommentListApiView.as_view(), name='movie-comments-list'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='movie-comments-detail'),
]
