import os
# 设置ｄｊａｎｇｏ配置
os.environ["DJANGO_SETTINGS_MODULE"]= "meiduo_mall.settings.dev"

from celery import Celery
# 实例对象
celery_app = Celery()
# 加载配置　指定消息队列使用redis
celery_app.config_from_object('celery_tasks.config')
# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])
# 自动识别任务
celery_app.autodiscover_tasks([
    'celery_tasks.sms',
])