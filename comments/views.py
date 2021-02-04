from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from notifications.signals import notify
from blog.models import Post
from django.contrib import messages
from .forms import CommentForm
from .models import Comment
import accounts.models
import markdown
import emoji
# Create your views here.


def comment(request, post_pk, parent_comment_id=None):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 这里我们使用了 django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post, pk=post_pk)
    # django 将用户提交的数据封装在 request.POST 中，这是一个类字典对象。
    # 我们利用这些数据构造了 CommentForm 的实例，这样就生成了一个绑定了用户提交数据的表单。
    request.session['comment_from'] = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            comment.text = markdown.markdown(comment.text,
                                             extensions=[
                                                 'markdown.extensions.extra',
                                                 'markdown.extensions.codehilite',
                                                 'markdown.extensions.toc',
                                             ])
            comment.text = emoji.emojize(comment.text, use_aliases=True)
            # 将评论和被评论的文章关联起来。
            comment.user = request.user
            comment.post = post
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                comment.parent_id = parent_comment.get_root().id
                # 被回复人
                comment.reply_to = parent_comment.user
                if not parent_comment.user.is_superuser and comment.user != comment.reply_to:
                    notify.send(
                        comment.user,
                        recipient=comment.reply_to,
                        verb='回复了你',
                        target=comment.post,
                        action_object=comment,
                    )
            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            comment.save()
            if not request.user.is_superuser and comment.user != comment.reply_to:
                notify.send(
                    request.user,
                    recipient=User.objects.filter(is_superuser=1),
                    verb='回复了你',
                    target=comment.post,
                    action_object=comment,
                )
            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            messages.add_message(request, messages.SUCCESS,
                                 '评论发表成功', extra_tags='success')
            return redirect(post)
        # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
        # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
        messages.add_message(request, messages.ERROR,
                             '发表评论失败', extra_tags='danger')
        return HttpResponseRedirect(request.session['comment_from'])
