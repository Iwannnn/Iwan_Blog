from django import template
from ..forms import CommentForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/_form.html', takes_context=True)
def show_comment_form(context, post, form=None, parent_comment=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }


@register.inclusion_tag('comments/inclusions/_list.html', takes_context=True)
def show_comments(context, user, post, form=None):
    comment_list = post.comment_set.all().order_by(
        'tree_id', 'created_time')  # 获取全部评论
    comments_count = comment_list.count()
    if form is None:
        form = CommentForm()
    return {
        'comment_count': comments_count,
        'comment_list': comment_list,
        'form': form,
        'post': post,
        'user': user,
    }
