from django.urls import path,re_path
from apps.user import views
urlpatterns = [
    # 用户注册
    re_path(r'^register/$', views.RegisterView.as_view(),name="register"),
    # 用户名查重
    re_path(r'^username/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view()),
    # 电话号查重
    re_path(r'^mobile/(?P<mobile>1[345789]\d{9})/count/$', views.MobileCountView.as_view()),
    # 图形验证码
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
    # 检验验证码
    re_path(r'^check_image_codes/$', views.ImageCodeCheckView.as_view()),
    # 用户登录
    re_path(r'^login/$',views.LoginView.as_view(),name="login"),
    # 用户个人信息
    re_path(r'^ownInformation/$',views.OwnInformationView.as_view(),name="owninformation"),
    # 注销账号
    re_path(r'^logout/$', views.LogOutView.as_view(), name="logout"),
]