from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


class Comment(MPTTModel):
    user = models.ForeignKey(
        User, verbose_name='用户名', on_delete=models.CASCADE)
    text = MDTextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey(
        'blog.Post', verbose_name='文章', on_delete=models.CASCADE)  # 一个文章能有多个评论
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    class MPTTMeta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        order_insertion_by = ['tree_id']

    def __str__(self):
        return '{}: {}'.format(self.user, self.text[:20])
