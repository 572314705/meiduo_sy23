from meiduo_mall.libs.yuntongxun.sms import CCP
from celery_tasks.main import celery_app

@celery_app.task(name='send_sms',bind=True,retry_backoff=3)
def send_sms(self,to,datas,tempid):
    try:
        # ccp = CCP()
        # ccp.send_template_sms(mobile,[sms_code,constants.SMS_CODE_EXPIRES],1)
        print(datas[0])
    except Exception as e:
        # 当失败是　任务重试
        self.retry(exc=e,max_retries=2)