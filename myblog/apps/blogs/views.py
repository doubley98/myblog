import datetime
import json

from django import http
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View

from apps.blogs.models import Blogs
from apps.comments.models import Comments


class DetailView(View):
    def get(self, request, blogId):
        if not blogId:
            return http.JsonResponse({"status": 402, "msg": "参数获取失败"})

        try:
            blog = Blogs.objects.filter(blog_id=blogId).first()
        except Exception as e:
            return http.JsonResponse({"status": 402, "msg": "blog数据获取异常"})
        if blog is None:
            return http.JsonResponse({"status": 402, "msg": "不存在该blog"})
        blogObj = {
            "title": blog.blog_title,
            "author": blog.author,
            "content": blog.content,
            "createtime": blog.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }

        return render(request, "detail.html", context={"blogList": json.dumps(blogObj)})


class OwnBLogView(View):
    def get(self, request):
        username = request.user.username
        if not username:
            return redirect(reverse("user:login"))
        try:
            blogs = Blogs.objects.filter(author=username).order_by("-pk").all()
        except Exception as e:
            return http.JsonResponse({"status": 402, "msg": "获取用户数据失败"})
        blogList = []
        for blog in blogs:
            blogList.append({
                "id": blog.blog_id,
                "title": blog.blog_title,
                "author": blog.author,
                "createtime": blog.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return render(request, "ownblog.html", context={"status": 200, "blogList": json.dumps(blogList)})


class AddBlogView(View):
    def get(self, request):
        return render(request, "addblog.html")

    def post(self, request):
        if not request.user.username:
            return http.JsonResponse({"status": 402, "msg": "请先进行登陆"})
        
        title = json.loads(request.body.decode()).get("title")
        content = json.loads(request.body.decode()).get("content")
        author = request.user.username

        if not all([title, content, author]):
            return http.JsonResponse({"status": 402, "msg": "参数缺失"})
        if len(title) > 50:
            return http.JsonResponse({"status": 402, "msg": "文章标题请限制在50个字符之间"})
        if len(content) > 10000:
            return http.JsonResponse({"status": 402, "msg": "文章内容请限制在10000个字符之间"})

        try:
            Blogs.objects.create(blog_title=title, author=author, content=content)
        except Exception as e:
            return http.JsonResponse({"status": 402, "msg": "创建失败 请检查是否登陆"})
        return http.JsonResponse({"status": 200, "msg": "添加成功"})


class BlogsListView(View):
    def get(self, request):
        try:
            blogs = Blogs.objects.filter().order_by("-pk").all()
        except Exception as e:
            return JsonResponse({"status": 402, "msg": "获取数据失败"})
        blogList = []
        for blog in blogs:
            blogList.append({
                "id": blog.blog_id,
                "title": blog.blog_title,
                "author": blog.author,
                "createtime": blog.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })
        return render(request, "main.html", context={"status": 200, "blogList": json.dumps(blogList)})


class SearchListView(View):
    def get(self, request):
        keyword = request.GET.get("keyword")
        try:
            searchlist = Blogs.objects.filter(Q(blog_title__contains=keyword) | Q(author__contains=keyword)).order_by(
                "-pk").all()
        except Exception as e:
            return JsonResponse({"status": 402, "msg": "获取数据失败"})

        blogList = []
        for blog in searchlist:
            blogList.append({
                "id": blog.blog_id,
                "title": blog.blog_title,
                "author": blog.author,
                "createtime": blog.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse({"status": 200, "blogList": blogList})
