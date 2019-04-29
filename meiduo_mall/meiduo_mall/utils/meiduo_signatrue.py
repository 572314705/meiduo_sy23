from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings


def dumps(json, expires):
    # 加密
    # 1.创建对象
    Serializer(settings.SECRET_KEY, expires)
    # ２．加密
    json_str = Serializer.dumps(json)
    # ３．返回字符串
    return json_str.decode()


def loads(json_str, expires):
    # 解密
    # 　１．创建对象
    Serializer(settings.SECRET_KEY, expires)
    # 　２．解密
    json = Serializer.loads(json_str)
    # 　３．返回字符串
    return json

    pass
