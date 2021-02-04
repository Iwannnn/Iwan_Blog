from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.utils.functional import cached_property
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from mdeditor.fields import MDTextField
import re
import markdown
import emoji
from markdown import extensions
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField('标题', max_length=100)
    body = MDTextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    summary = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(
        Category, verbose_name='分类', on_delete=models.CASCADE)
    # 实现一个类型对应多个文章（一对多） 级联删除
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # 实现一个标签对应多个文章 一个文章对应对各标签（多对多）
    author = models.ForeignKey(
        User, verbose_name='作者', on_delete=models.CASCADE)
    # 实现一个作者对应多个文章（一对多） 级联删除
    views = models.PositiveIntegerField(default=0, editable=False)
    image = models.ImageField(upload_to='post/%Y%m%d/', blank=True)
    likes = models.PositiveIntegerField(default=0)
    image_resize = ImageSpecField(
        source="image",
        processors=[ResizeToFill(600, 400)],  # 处理后的图像大小
        format='JPEG',  # 处理后的图片格式
        options={'quality': 95}  # 处理后的图片质量
    )

    class Meta:
        ordering = ("-created_time",)
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',  # 自动生成目录
            TocExtension(slugify=slugify),
        ])
        self.summary = strip_tags(md.convert(self.body))[:122]
        super().save(*args, **kwargs)

    def get_absolute_url(self):  # 生成url
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    @property
    def toc(self):
        return self.rich_content.get("toc", "")

    @property
    def body_html(self):
        return self.rich_content.get("content", "")

    @cached_property
    def rich_content(self):  # 以属性访问的形式获取返回值 提供缓存功能
        return generate_rich_content(self.body)

    def __str__(self):
        return self.title


def generate_rich_content(value):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    content = emoji.emojize(content, use_aliases=True)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ""
    return {"content": content, "toc": toc}
