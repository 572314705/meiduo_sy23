from django.conf.urls import url
from . import views
urlpatterns = [
    url('^image_codes/d4de5b16-1176-476a-ba34-5219a645a65c/$',views.ImageCodeView.as_view())
]