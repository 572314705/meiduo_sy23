from django.shortcuts import render
from django.views import View
from django import http
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from meiduo_mall.utils.response_code import RETCODE
from .models import OAuthQQUser
from meiduo_mall.utils import meiduo_signatrue
from .constants import OPENID_EXPIRES

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
                token = meiduo_signatrue.dumps({'openid':openid},OPENID_EXPIRES)
                # 　展示页面
                context = {'token': token}
                return render(request, 'oauth_callback.html', context)
            else:
                # 查找到绑定的用户，就状态保持
                pass
        except:
            openid = 0
        return http.HttpResponse(openid)

    def post(self, request):
        # 接收用户填写的数据，进行绑定

        pass
