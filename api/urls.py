from django.urls import path, include

from api.users.views import RegisterUserView


urlpatterns = [
    path('/blog', include('api.blogs.urls')),
    path('/user/registration/', RegisterUserView.as_view())
]