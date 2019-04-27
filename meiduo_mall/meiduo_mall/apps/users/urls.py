from django.conf.urls import url

from . import views

from django.contrib.auth.decorators import login_required
urlpatterns = [
    url(r'^register/$', views.RegisterView.as_view()),
    url(r'^usernames/(?P<username>[a-zA-Z0-9-_]{5,20})/count/$', views.UsernameCheckView.as_view()),
    url(r'^mobiles/(?P<mobile>1[345789]\d{9})/count/$', views.MobileCheckView.as_view()),
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
    # login_required装饰器 判断用户是否登录
    # url(r'^info/$', login_required(views.InfoView.as_view())),
    url(r'^info/$', views.InfoView.as_view()),
]
