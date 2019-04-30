from django.shortcuts import render
from django.views import View
from meiduo_mall.utils.response_code import RETCODE
from django import http
from .models import Area


class AreasView(View):
    """省市区数据"""

    def get(self, request):
        # 接收
        area_id = request.GET.get('area_id')
        # 验证 : area_id　允许为空，表示查询省信息
        # 处理
        if area_id is None:
            # 查询省信息
            provinces = Area.objects.filter(parent__isnull=True)
            # 转换成字典
            province_list = []
            for province in provinces:
                province_list.append({
                    'id' : province.id,
                    'name':province.name,
                })

            return http.JsonResponse({
                'code':RETCODE.OK,
                'errmsg':'ok',
                'province_list':province_list,
            })
        else:
            # 查询指定编码地区及子及地区
            try:
                area = Area.objects.get(pk = area_id)
            except:
                return http.JsonResponse({
                    'code':RETCODE.PARAMERR,
                    'errmsg':'地区编码无效',

                })
            else:
                # 获取子级地区
                subs = area.subs.all()
                sub_list = []
                for sub in subs:
                    sub_list.append({
                        'id':sub.id,
                        'name':sub.name
                    })
                # 结果数据
                sub_data = {
                    'id':area.id,
                    'name':area.name,
                    'subs':sub_list

                }
                return http.JsonResponse({
                    'code':RETCODE.OK,
                    'errmsg':'ok',
                    'sub_data':sub_data
                })
                # 响应
