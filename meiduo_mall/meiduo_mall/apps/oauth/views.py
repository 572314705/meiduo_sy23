from django.shortcuts import render
from django.views import View
from django import http

class QQurlView(View):
    def get(self,request):
        # 生成授权地址
        pass

class QQopenidView(View):
    def get(self,request):
        # 获取openid
        pass
