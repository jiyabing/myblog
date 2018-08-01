from django.http import HttpResponse
from pure_pagination import PageNotAnInteger, Paginator
from django.shortcuts import render

from blog.forms import CommentForm
from blog.models import Blog, Tag, Category, Comment, Counts
import markdown

# Create your views here.


def index(request):
    """
    首页
    """
    all_blog = Blog.objects.all().order_by('-id')
    # 博客、标签、分类数目统计
    count_nums = Counts.objects.get(id=1)
    blog_nums = count_nums.blog_nums
    cate_nums = count_nums.category_nums
    tag_nums = count_nums.tag_nums
    for blog in all_blog:
        blog.content = markdown.markdown(blog.content)
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(all_blog, 2, request=request)  # 2为每页展示的博客数目
    all_blog = p.page(page)
    return render(request, 'index.html', {
        'all_blog': all_blog,
        'blog_nums': blog_nums,
        'cate_nums': cate_nums,
        'tag_nums': tag_nums,
    })


def archive(request):
    """
    归类
    """
    all_blog = Blog.objects.all().order_by('-create_time')
    # 博客、标签、分类数目统计
    count_nums = Counts.objects.get(id=1)
    blog_nums = count_nums.blog_nums
    cate_nums = count_nums.category_nums
    tag_nums = count_nums.tag_nums
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(all_blog, 3, request=request)
    all_blog = p.page(page)
    return render(request, 'archive.html', {
        'all_blog': all_blog,
        'blog_nums': blog_nums,
        'cate_nums': cate_nums,
        'tag_nums': tag_nums,
    })


def tags(request):
    """
    标签云
    """
    all_tag = Tag.objects.all()
    # 博客、标签、分类数目统计
    count_nums = Counts.objects.get(id=1)
    blog_nums = count_nums.blog_nums
    cate_nums = count_nums.category_nums
    tag_nums = count_nums.tag_nums
    return render(request, 'tags.html', {
        'all_tag': all_tag,
        'blog_nums': blog_nums,
        'cate_nums': cate_nums,
        'tag_nums': tag_nums,
    })


def tag_detail(request, tag_name):
    """
    标签下的所有博客
    """
    tag = Tag.objects.filter(name=tag_name).first()
    tag_blog = tag.blog_set.all()
    # 博客、标签、分类数目统计
    count_nums = Counts.objects.get(id=1)
    blog_nums = count_nums.blog_nums
    cate_nums = count_nums.category_nums
    tag_nums = count_nums.tag_nums
    # 分页
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(tag_blog, 2, request=request)
    tag_blog = p.page(page)
    return render(request, 'tag-detail.html', {
        'tag_blog': tag_blog,
        'tag_name': tag_name,
        'blog_nums': blog_nums,
        'cate_nums': cate_nums,
        'tag_nums': tag_nums,
    })


def blog_detail(request, blog_id):
    """
    博客详情页
    """
    blog = Blog.objects.get(id=blog_id)
    # 博客、标签、分类数目统计
    count_nums = Counts.objects.get(id=1)
    blog_nums = count_nums.blog_nums
    cate_nums = count_nums.category_nums
    tag_nums = count_nums.tag_nums
    # markdown格式化博客内容
    blog.content = markdown.markdown(blog.content)
    # 获取评论内容
    all_comment = Comment.objects.filter(blog_id=blog_id)
    comment_nums = all_comment.count()
    # 实现博客上一篇与下一篇功能
    has_prev = False
    has_next = False
    id_prev = id_next = int(blog_id)
    blog_id_max = Blog.objects.all().order_by('-id').first()
    id_max = blog_id_max.id
    blog_prev = ''
    blog_next = ''
    while not has_prev and id_prev >= 1:
        blog_prev = Blog.objects.filter(id=id_prev-1).first()
        if not blog_prev:
            id_prev -= 1
        else:
            has_prev = True
    while not has_next and id_next <= id_max:
        blog_next = Blog.objects.filter(id=id_next+1).first()
        if not blog_next:
            id_next += 1
        else:
            has_next = True
    return render(request, 'blog-detail.html', {
        'blog': blog,
        'blog_prev': blog_prev,
        'blog_next': blog_next,
        'has_prev': has_prev,
        'has_next': has_next,
        'all_comment': all_comment,
        'comment_nums': comment_nums,
        'blog_nums': blog_nums,
        'cate_nums': cate_nums,
        'tag_nums': tag_nums,
    })


def add_comment(request):
    """
    添加评论
    """
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment_form.save()
        return HttpResponse('{"status": "success"}', content_type='application/json')
    else:
        return HttpResponse('{"status": "fail"}', content_type='application/json')


def category_detail(request, category_name):
    """
    类别下的所有博客
    """
    category = Category.objects.filter(name=category_name).first()
    cate_blog = category.blog_set.all()
    # 博客、标签、分类数目统计
    count_nums = Counts.objects.get(id=1)
    blog_nums = count_nums.blog_nums
    cate_nums = count_nums.category_nums
    tag_nums = count_nums.tag_nums
    # 分页
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(cate_blog, 2, request=request)
    cate_blog = p.page(page)
    return render(request, 'category-detail.html', {
        'cate_blog': cate_blog,
        'category_name': category_name,
        'blog_nums': blog_nums,
        'cate_nums': cate_nums,
        'tag_nums': tag_nums,
    })
