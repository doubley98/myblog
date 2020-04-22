import re
from django.contrib.auth.backends import ModelBackend

from apps.user.models import Users


def get_user_by_account(account):
    try:
        if re.match('^1[345789]\d{9}$', account):
            user = Users.objects.get(mobile=account)
        else:
            user = Users.objects.get(username=account)

    except Users.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if request is None:
            try:
                user = Users.objects.get(username=username, is_staff=True)
            except:
                return None
            if user.check_password(password):
                return user
            else:
                return None
        else:
            # 3. 实现多账号 校验用户名和 手机号
            user = get_user_by_account(username)

            # 校验密码是否正确
            if user and user.check_password(password):
                return user
            else:
                return None