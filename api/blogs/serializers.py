
import filetype
from django.contrib.auth import get_user_model
from rest_framework      import serializers

from .models import Category, File, Post, PostFile, PostTag, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'nickname', 'email')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=False)

    class Meta:
        model = PostTag
        exclude = ('post',)
        

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class PostFileSerializer(serializers.ModelSerializer):
    file = FileSerializer(many=False)

    class Meta:
        model = PostFile
        exclude = ('post',)


class BlogPostReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    author = UserSerializer(many=False)
    tags = PostTagSerializer(many=True, source='posttag_set')
    files = PostFileSerializer(many=True, source='postfile_set')
    
    class Meta:
        model = Post
        fields = '__all__'


class BlogPostCreationSerializer(serializers.ModelSerializer):
    tags = serializers.ListSerializer(child=serializers.CharField(), write_only=True)
    files = serializers.ListSerializer(child=serializers.FileField(), write_only=True)
    
    class Meta:
        model = Post
        exclude = ('is_active', 'author')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        files = validated_data.pop('files')
        new_post        = self.Meta.model(**validated_data)
        new_post.author = self.context['request'].user
        new_post.save()

        for tag in tags :
            tag_obj, _ = Tag.objects.get_or_create(name=tag)
            PostTag.objects.create(tag=tag_obj, post=new_post)

        for file in files:
            mime = filetype.guess(file).mime
            mime = mime if mime is not None else 'unknown'
            new_file = File.objects.create(file=file, file_type=mime, name=file.name)
            PostFile.objects.create(post=new_post, file=new_file)

        return new_post

    def to_representation(self, instance):
        return BlogPostReadSerializer(instance).data