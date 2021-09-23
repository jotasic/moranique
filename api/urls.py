from django.urls                    import path, include
from rest_framework.routers         import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .users.views import RegisterUserView
from .blogs.views import BlogPostView, BlogPostCreateView


router = DefaultRouter(trailing_slash=False)
router.register(r'blogs', BlogPostView)

urlpatterns = [
    path('/user/registration/', RegisterUserView.as_view(), name='registration'),
    path('/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('/', include(router.urls), name='blogs'),
    path('/blog/create', BlogPostCreateView.as_view(), name='create post'),
]