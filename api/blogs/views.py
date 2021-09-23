import json

from rest_framework                import status, parsers
from rest_framework.response       import Response
from rest_framework.viewsets       import ReadOnlyModelViewSet
from rest_framework.generics       import CreateAPIView
from rest_framework.permissions    import IsAuthenticated
from rest_framework.pagination     import LimitOffsetPagination
from rest_framework_simplejwt      import authentication
from django_filters                import CharFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import BlogPostReadSerializer, BlogPostCreationSerializer
from .models      import Post


class MultipartJsonParser(parsers.MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context
        )
        data = {}

        for key, value in result.data.items():
            if type(value) != str:
                data[key] = value
                continue
            if '{' in value or "[" in value:
                try:
                    data[key] = json.loads(value)
                except ValueError:
                    data[key] = value
            else:
                data[key] = value

        return parsers.DataAndFiles(data, result.files)


class BlogPostListFilter(FilterSet):
    title    = CharFilter(lookup_expr='icontains')
    category = CharFilter(lookup_expr='icontains', field_name='category__name')
    tag      = CharFilter(lookup_expr='icontains', field_name='posttag__tag__name')

    class Meta:
        model  = Post
        fields = ('title', 'category', 'tag', )


class BlogPostView(ReadOnlyModelViewSet):
    serializer_class   = BlogPostReadSerializer
    pagination_class   = LimitOffsetPagination
    filter_backends    = (DjangoFilterBackend, )
    filterset_class    = BlogPostListFilter
    queryset           = Post.objects.filter(is_active=True)\
                            .select_related('category', 'author')\
                            .prefetch_related('posttag_set', 'posttag_set__tag',\
                                            'postfile_set', 'postfile_set__file')


class BlogPostCreateView(CreateAPIView):
    permission_classes      = (IsAuthenticated, )
    authentication_classes = (authentication.JWTAuthentication, )
    serializer_class = BlogPostCreationSerializer
    parser_classes = (MultipartJsonParser, )

    def create(self, request, *args, **kwargs):
        data = request.data

        data['files'] = request.FILES.getlist('files')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)