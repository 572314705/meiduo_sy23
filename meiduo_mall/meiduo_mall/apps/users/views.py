from django.shortcuts import render

from django.views import View

class RegisterView(View):
    def get(self,request):
        '''响应试图页面'''
        # 1.接收
        # 2.处理
        # 3.验证
        # 3.响应　：展示处理页面
        return render(request,'register.html')
    def post(self,request):
        '''创建用户对象，保存在表中'''
        # 1.接收
        # 2.处理
        # 3.验证
        # 3.响应
        pass