from django.shortcuts import render

from django.views import View
from meiduo_mall.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . import constants
from django import http
from meiduo_mall.utils.response_code import RETCODE
import random
from meiduo_mall.libs.yuntongxun.sms import CCP


class ImageCodeView(View):
    '''生成图片'''
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


class SmsCodeView(View):
    '''短信验证'''
    def get(self, request, mobile):
        # 接收
        image_code_request = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 验证: 图形验证
        # １．１读取ｒｅｄｉｓ中的图形验证码
        redis_cli = get_redis_connection('verify')  # 连接redis数据库
        image_code_redis = redis_cli.get(uuid)

        # １．２判断是否为空　因为超时，redis数据库中存储的图形已失效
        if image_code_redis is None:
            return http.JsonResponse({
                'code':RETCODE.IMAGECODEERR,
                'errmsg':'图形已经失效',
            })
        # １．３
        # 注意１：redis中存储的类型是ｂｙｔｅｓ
        # 注意２: 不去分打小写
        if image_code_request.upper() != image_code_redis.decode():
            return http.JsonResponse({
                'code':RETCODE.IMAGECODEERR,
                'errmsg':'图形错误',
            })

        # 1.4 强制图形验证码过期
        redis_cli.delete(uuid)

        # 　处理
        # 1.生成随机的六位数
        sms_code ='%06d' % random.randint(0,999999)
        # 2. 保存到redis中
        redis_cli.setex('sms'+ mobile,constants.SMS_CODE_EXPIRES,sms_code)
        # # 3. 发短信
        # ccp = CCP()
        # ccp.send_template_sms(mobile,[sms_code,constants.SMS_CODE_EXPIRES],1)
        print(sms_code)
        # 响 应
        return http.JsonResponse({
            'code':RETCODE.OK,
            'errmsg':'OK',
        })

