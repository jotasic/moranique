from django.urls            import path, include
from rest_framework.routers import DefaultRouter

from api.users.views import RegisterUserView
from api.blogs.views import BlogPostView, BlogPostCreateView


router = DefaultRouter(trailing_slash=False)
router.register(r'blogs', BlogPostView)

urlpatterns = [
    path('/', include(router.urls), name='blogs'),
    path('/blog/create', BlogPostCreateView.as_view(), name='create post'),
    path('/user/registration/', RegisterUserView.as_view(), name='registration'),
]