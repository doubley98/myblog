from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^blogList/$', views.BlogsListView.as_view(),name="bloglist"),
    re_path(r'^searchList/$', views.SearchListView.as_view()),
    re_path(r'^addBlog/$',views.AddBlogView.as_view(),name="addblog"),
    re_path(r'^ownBlog/$',views.OwnBLogView.as_view(),name="ownblog"),
    re_path(r'^detail/(?P<blogId>\d+)$',views.DetailView.as_view()),
]
