import json

import re
from django import http
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse

# Create your views here.
from django.urls import reverse
from django.views import View
from django_redis import get_redis_connection

from apps.user.models import Users
from libs.captcha.captcha import captcha


class LogOutView(View):
    def get(self, request):
        from django.contrib.auth import logout
        logout(request)
        response = redirect(reverse('blog:bloglist'))
        response.delete_cookie('username')
        return response


class OwnInformationView(View):
    def get(self,request):
        user = request.user
        username = user.username
        if not username:
            return redirect(reverse("user:login"))
        information = {
            "username": user.username,
            "mobile": user.mobile,
            "email": user.email,
            "date_joined": user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        }
        print(information)
        return render(request,"owninformation.html",context={"information":json.dumps(information)})


class LoginView(View):
    def get(self,request):
        return render(request,"login.html")
    def post(self, request):
        username = json.loads(request.body.decode()).get("username")
        password = json.loads(request.body.decode()).get("password")
        remember = json.loads(request.body.decode()).get("remember")

        if not all([username, password]):
            return JsonResponse({"status": 402, "msg": "缺少参数"})
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({"status": 402, "msg": '请输入5-20个字符的用户名'})
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({"status": 402, "msg": '请输入8-20位的密码'})

        from django.contrib.auth import authenticate, login
        try:
            user = authenticate(request, username=username, password=password)
        except Exception as e:
            return JsonResponse({"status": 402, "msg": "获取数据失败"})

        if user is None:
            return JsonResponse({"status": 402, "msg": "请重新核对用户名和密码"})

        login(request, user)
        response = JsonResponse({"status": 200, "msg": "登录成功"})
        if remember is False:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)
        response.set_cookie('username', user.username, max_age=14 * 24 * 3600)

        return response


class RegisterView(View):
    def get(self,request):
        return render(request,"register.html")
    def post(self, request):
        username = json.loads(request.body.decode()).get("username")
        password = json.loads(request.body.decode()).get("password")
        mobile = json.loads(request.body.decode()).get("mobile")
        allow = json.loads(request.body.decode()).get("allow")

        if not all([username, password, mobile, allow]):
            return http.JsonResponse({"status": 402, "msg": "缺少参数"})

        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return http.JsonResponse({"status": 402, "msg": "请输入5-20个字符的用户名"})

        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return http.JsonResponse({"status": 402, "msg": "请输入8-20个数字字母"})

        if not re.match(r'^1[345789]\d{9}$', mobile):
            return http.JsonResponse({"status": 402, "msg": "手机号格式有误"})

        if allow is not True:
            return http.JsonResponse({"status": 402, "msg": "请勾选协议"})

        try:
            Users.objects.create_user(username=username, password=password, mobile=mobile)
        except Exception as e:
            return JsonResponse({"status": 402, "msg": "获取数据失败"})
        

        return JsonResponse({"status": 200, "msg": "注册成功"})


class UsernameCountView(View):
    def get(self, request, username):
        try:
            count = Users.objects.filter(username=username).count()
        except Exception as e:
            return JsonResponse({"status": 402, "msg": "获取数据失败"})
        return http.JsonResponse({'status': 200, 'msg': 'OK', 'count': count})


class MobileCountView(View):
    def get(self, request, mobile):
        try:
            count = Users.objects.filter(mobile=mobile).count()
        except Exception as e:
            return JsonResponse({"status": 402, "msg": "获取数据失败"})

        return http.JsonResponse({'status': 200, 'msg': 'OK', 'count': count})


class ImageCodeView(View):
    def get(self, request, uuid):
        # 实例化 返回的是图形和验证码，分别用两个变量接收
        text, image = captcha.generate_captcha()
        # 存在redis数据库中 数据库名为verify_image_code
        redis_client = get_redis_connection('verify_image_code')
        # 图片验证码过期时间
        IMAGE_CODE_REDIS_EXPIRES = 5 * 60
        # 存储缓存数据，setex（‘key（这里统一在前面加了前缀）’，缓存时间（这里把时间封装成了一个常量，需要导入，值（这里用的是验证码的值））
        redis_client.setex('img_%s' % uuid, IMAGE_CODE_REDIS_EXPIRES, text)

        # 返回一个响应对象，这个对象是一个图片，也就是一个二进制流
        return http.HttpResponse(image, content_type='image/jpg')


class ImageCodeCheckView(View):
    def post(self, request):
        # 由于接收过来的是bytes类型，进行解码,再由json转为字典
        image_code = json.loads(request.body.decode()).get('image_code')
        uuid = json.loads(request.body.decode()).get('image_code_id')

        # 链接redis
        image_client = get_redis_connection('verify_image_code')
        redis_img_code = image_client.get('img_%s' % uuid)

        # 从redis中取出验证码进行比对
        if not redis_img_code:
            return http.JsonResponse({"status": "402", "msg": "图形验证码失效了"})

        image_client.delete('img_%s' % uuid)
        if image_code.lower() != redis_img_code.decode().lower():
            return http.JsonResponse({"status": "402", "msg": "输入图形验证码有误"})

        return http.JsonResponse({"status": "200", "msg": "验证成功"})
