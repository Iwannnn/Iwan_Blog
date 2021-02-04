from .models import Post, Category, Tag
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.views.generic import ListView, DetailView
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
from django.db.models import Q
# Create your views here.


# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(PaginationMixin, ListView):
    Post.objects.all().order_by('-created_time')
    model = Post  # 指定从数据库获取的模型
    template_name = 'blog/index.html'
    context_object_name = 'post_list'  # 保存到post_list中
    # 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少篇文章
    paginate_by = 10


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(IndexView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    def get_queryset(self):
        t = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(IndexView, self).get_queryset().filter(tags=t)


class ArchiveView(IndexView):
    def get_queryset(self):
        return super(IndexView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                                            created_time__month=self.kwargs.get('month'))


class PostLikesView(IndexView):
    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=kwargs.get('id'))
        post.likes += 1
        post.save()
        return HttpResponse('success')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    # def get_object(self, queryset=None):
    #     post = super().get_object(queryset=None)
    #     md = markdown.Markdown(extensions=[
    #         'markdown.extensions.extra',
    #         'markdown.extensions.codehilite',
    #         TocExtension(slugify=slugify),
    #     ])
    #     post.body = md.convert(post.body)

    #     m = re.search(
    #         r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    #     post.toc = m.group(1) if m is not None else ''
    #     return post


def search(request):
    q = request.GET.get('q')
    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR,
                             error_msg, extra_tags='danger')
        return redirect('blog:index')
    post_list = Post.objects.filter(
        Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})


# def detail(request, pk):  # 根据url捕获文章id
#     post = get_object_or_404(Post, pk=pk)  # 匹配id
#     md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',  # 基础扩展
#         'markdown.extensions.codehilite',  # 代码高亮
#         'markdown.extensions.toc',  # 自动生成目录
#         TocExtension(slugify=slugify),
#     ])
#     post.body = md.convert(post.body)
#     m = re.search(
#         r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = m.group(1) if m is not None else ''
#     return render(request, 'blog/detail.html', context={'post': post})

# def archive(request, year, month):
#     post_list = Post.objects.filter(
#         created_time__year=year, created_time__month=month).order_by('-created_time')  # 使用filter过滤文章
#     return render(request, 'blog/index.html', context={'post_list': post_list})

# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})

# def tag(request, pk):
#     t = get_object_or_404(Tag, pk=pk)
#     post_list = Post.objects.filter(tags=t).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})
