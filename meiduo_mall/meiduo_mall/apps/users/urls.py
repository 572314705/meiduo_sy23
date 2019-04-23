from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^register/$',views.RegisterView.as_view()),
    url(r'^usernames/(?P<username>[a-zA-Z0-9-_]{5,20})/count/$',views.UsernameCheckView.as_view()),
]