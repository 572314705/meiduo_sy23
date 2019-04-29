from django.shortcuts import render, redirect
from django.views import View
from django import http
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from meiduo_mall.utils.response_code import RETCODE
from .models import OAuthQQUser
from meiduo_mall.utils import meiduo_signatrue
from .constants import OPENID_EXPIRES
from users.models import User
from django.contrib.auth import login


class QQurlView(View):
    def get(self, request):
        # 生成授权地址
        next_url = request.GET.get('next')
        # 1.创建工具对象
        qq_tool = OAuthQQ(
            settings.QQ_CLIENT_ID,
            settings.QQ_CLIENT_SECRET,
            settings.QQ_REDIRECT_URI,
            next_url
        )
        # 2.调用方法，生成url地址
        login_url = qq_tool.get_qq_url()
        # 响应
        return http.JsonResponse({
            'code': RETCODE.OK,
            'errmsg': 'OK',
            'login_url': login_url
        })


class QQopenidView(View):
    def get(self, request):
        # 获取openid
        # 1.接收code参数,
        code = request.GET.get('code')
        next_url = request.GET.get('state')
        # 2. 创建一个工具对象
        qq_tool = OAuthQQ(
            settings.QQ_CLIENT_ID,
            settings.QQ_CLIENT_SECRET,
            settings.QQ_REDIRECT_URI,
            next_url
        )
        try:
            # 3.生成token
            token = qq_tool.get_access_token(code)
            # 4.生成openid
            openid = qq_tool.get_open_id(token)

            # 用openid判断是否绑定过ＱＱ用户
            try:

                qq_user = OAuthQQUser.objects.get(openid=openid)
            except:
                # 没有绑定，就返回一个绑定页面,初次绑定
                # 加密
                token = meiduo_signatrue.dumps({'openid': openid}, OPENID_EXPIRES)
                # 　展示页面
                context = {'token': token}
                return render(request, 'oauth_callback.html', context)
            else:
                # 查找到绑定的用户，就状态保持
                login(request,qq_user.user)
                response = redirect(next_url)
                response.set_cookie('username',qq_user.user.username)
                return response
        except:
            openid = 0
        return http.HttpResponse(openid)

    def post(self, request):
        # 接收用户填写的数据，进行绑定
        # 接收
        mobile = request.POST.get('mobile')
        pwd = request.POST.get('pwd')
        pic_code = request.POST.get('pic_code')
        sms_code = request.POST.get('sms_code')
        token = request.POST.get('access_token')

        # 验证 ：非空　格式　短信验证　与注册相同　不再重复
        # 解密openid

        json = meiduo_signatrue.loads(token, OPENID_EXPIRES)
        if json is None:
            return http.HttpResponseBadRequest('授权信息已经过期')
        openid = json.get('openid')
        # 处理
        # 1.根据手机号查询用户对象
        try:
            user = User.objects.get(mobile=mobile)
        except:
            # 　2.如果为查询到对象，则新建用户对象
            user = User.objects.create_user(username=mobile, password=pwd, mobile=mobile)
        else:
            # 3.如果查询到用户对象，则判断密码
            if not user.check_password(pwd):
                # 3.1如果密码错误，则提示
                return http.HttpResponseBadRequest('帐号密码错误')
        # 3.2如果密码正确则得到用户对象

        # 4.绑定：　创建一个OAuthQQUser对像
        OAuthQQUser.objects.create(user=user, openid=openid)
        # 5.状态保持
        login(request, user)
        response = redirect('/')
        response.set_cookie('username',user.username,max_age=60*6)
        # 响应
        return response
