from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count
from blog.models import Category
register = template.Library()  # 实例化


# 装饰函数
# take_contexts 传入模板变量和父模板
# 最近文章
@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num]
    }

# 归档模板


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
    }

# 分类模板


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(
        num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }

# 标签模板


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(
        num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }
