from django.contrib import admin
from .models import Post, Category, Tag
from django.utils import timezone

# Register your models here.


class PostAdmin (admin.ModelAdmin):
    list_display = ['title', 'created_time',
                    'modified_time', 'views', 'category', 'author']
    fields = ['title', 'body', 'image', 'summary', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
