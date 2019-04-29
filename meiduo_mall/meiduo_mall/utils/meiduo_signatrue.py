from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings


def dumps(json, expires):
    # 加密
    # 1.创建对象
    serializer=Serializer(settings.SECRET_KEY, expires)
    # ２．加密-bytes类型数据
    json_str = serializer.dumps(json)
    # ３．返回字符串-需要解码
    return json_str.decode()


def loads(json_str, expires):
    # 解密
    # 　１．创建对象
    serializer=Serializer(settings.SECRET_KEY, expires)
    # 　２．解密
    try:
        json = serializer.loads(json_str)
    except:
    # 如果字符串被修改，或过期，解密时会抛异常
        return None

    else:
        # 　３．返回字符串
        return json

