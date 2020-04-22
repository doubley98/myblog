import json

from django import http
from django.shortcuts import render,redirect
from django.urls import reverse

# Create your views here.
from django.views import View

from apps.blogs.models import Blogs
from apps.comments.models import Comments


class DelCommentView(View):
    def post(self, request):
        com_id = json.loads(request.body.decode()).get("com_id")
        if com_id is None:
            return http.JsonResponse({"status": 402, "msg": "缺少参数"})
        try:
            Comments.objects.filter(com_id=com_id).delete()
        except Exception as e:
            return http.JsonResponse({"status": 402, "msg": "删除失败"})

        return http.JsonResponse({"status": 200, "msg": "删除成功"})


class OwnCommentsView(View):
    def get(self, request):
        username = request.user.username
        if not username:
            return redirect(reverse("user:login"))

        try:
            comments = Comments.objects.filter(username=username).order_by("-pk").all()
        except Exception as e:
            return http.JsonResponse({"status": 402, "msg": "获取评论信息失败"})

        owncomments = []
        if comments is None:
            owncomments = []
        else:
            for comment in comments:
                try:
                    blog = Blogs.objects.filter(blog_id=comment.blog_id).first()
                except Exception as e:
                    return http.JsonResponse({"status": 402, "msg": "获取评论文章信息失败"})
                owncomments.append({
                    "com_id": comment.com_id,
                    "content": comment.com_content,
                    "time": comment.createtime.strftime('%Y-%m-%d %H:%M:%S'),
                    "blog_title": blog.blog_title
                })

        return render(request, "owncomments.html", context={"owncomments": json.dumps(owncomments)})


class GetCommentsView(View):
    def get(self, request, blogId):
        try:
            comments = Comments.objects.filter(blog_id=blogId).all().order_by("-pk")
        except Exception as e:
            return http.JsonResponse({"status": 402, "msg": "comments数据获取异常"})
        commentList = []
        if not comments:
            commentList = []
        else:
            for comment in comments:
                commentList.append({
                    "username": comment.username,
                    "content": comment.com_content,
                    "createtime": comment.createtime.strftime('%Y-%m-%d %H:%M:%S')
                })

        return http.JsonResponse({"status": 200, "commentList": commentList})


class AddCommentView(View):
    def post(self, request):
        comment = json.loads(request.body.decode()).get("comment")
        blogId = json.loads(request.body.decode()).get("blogId")
        username = request.user.username
        if not username:
            return http.JsonResponse({"status": 402, "msg": "请先返回主页面登陆"})

        try:
            Comments.objects.create(com_content=comment, username=username, blog_id=blogId)
        except Exception as e:
            return http.JsonResponse({"status": 402, "msg": "添加评论失败"})

        return http.JsonResponse({"status": 200, "msg": "评论成功"})
