from django.shortcuts import render

from django.views import View
from meiduo_mall.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . import constants
from django import http


class ImageCodeView(View):
    def get(self, requset, uuid):
        # 接受
        # 验证
        # 处理
        # 1.生成字符／图片数据
        text, code, image = captcha.generate_captcha()
        # 2.保存字符
        # 2.1 连接redis
        redis_cli = get_redis_connection('verify')
        # 2.2 保存
        redis_cli.setex(uuid, constants.IMAGE_CODE_EXPIRES, code)
        # 响应　图片
        return http.HttpResponse(image, content_type='image/png')
