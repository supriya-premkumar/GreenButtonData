# encoding: utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from .views import home # might need to update
from fileupload.views import (
        BasicVersionCreateView, BasicPlusVersionCreateView,
        jQueryVersionCreateView, AngularVersionCreateView,
        PictureCreateView, PictureDeleteView, PictureListView,
        )

urlpatterns = [
    # AUTH
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),  # <- Here
    url(r'^$', home, name='home'),
    
    url(r'^basic/$', BasicVersionCreateView.as_view(), name='upload-basic'),
    url(r'^basic/plus/$', BasicPlusVersionCreateView.as_view(), name='upload-basic-plus'),
    url(r'^new/$', PictureCreateView.as_view(), name='upload-new'),
    url(r'^angular/$', AngularVersionCreateView.as_view(), name='upload-angular'),
    url(r'^jquery-ui/$', jQueryVersionCreateView.as_view(), name='upload-jquery'),
    url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), name='upload-delete'),
    url(r'^view/$', PictureListView.as_view(), name='upload-view'),
]
