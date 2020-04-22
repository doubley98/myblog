from django.urls import re_path
from . import views

urlpatterns = [
    # 添加评论
    re_path(r'^addComment/$', views.AddCommentView.as_view(), name="addcomment"),
    # 获取评论
    re_path(r'^getComments/(?P<blogId>\d+)/$', views.GetCommentsView.as_view(), name="getcomments"),
    # 获取个人评论
    re_path(r'^getOwnComments/$', views.OwnCommentsView.as_view(), name="owncomments"),
    # 删除评论
    re_path(r'^delComment/$',views.DelCommentView.as_view())
]
