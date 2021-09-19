from django.contrib import admin

from api.blogs.models import (
        Category, Tag, Post, 
        PostTags, File, PostFile
        )


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'edited_at',)    


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(PostTags)
admin.site.register(PostFile)
admin.site.register(File)
admin.site.register(Post, PostAdmin)