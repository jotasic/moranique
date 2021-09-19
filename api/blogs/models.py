from os import name
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table            = 'categories'
        verbose_name        = 'Category'
        verbose_name_plural = 'Categories'


class Post(models.Model):
    author_id   = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title       = models.CharField(max_length=255)
    content     = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    edited_at   = models.DateTimeField(auto_now=True)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table            = 'posts'
        verbose_name        = 'Post'
        verbose_name_plural = 'Posts'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}' 

    class Meta:
        db_table            = 'tags'
        verbose_name        = 'Tag'
        verbose_name_plural = 'Tags'


class PostTags(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    tag_id  = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.post_id} - {self.tag_id}'

    class Meta:
        db_table            = 'post_tags'
        verbose_name        = 'Post_tag'
        verbose_name_plural = 'Post_Tags'
   

class File(models.Model):
    url       = models.URLField()
    file_type = models.CharField(max_length=50)
    name      = models.CharField(max_length=255)

    class Meta:
        db_table            = 'files'
        verbose_name        = 'File'
        verbose_name_plural = 'Files'

    def __str__(self):
        return f'{self.name}: {self.url}'


class PostFile(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    file_id = models.ForeignKey(File, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.post_id} - {self.file_id}'

    class Meta:
        db_table            = 'post_files'
        verbose_name        = 'Post_file'
        verbose_name_plural = 'Post_Files'