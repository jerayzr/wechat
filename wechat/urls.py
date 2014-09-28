from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'wechat.views.wechat'),
    url(r'^userinfo/$', 'userinfo.views.user_judge'),
    url(r'^userinfo/signin/$', 'userinfo.views.user_signin'),
    url(r'^userinfo/info/$', 'userinfo.views.user_info'),
)
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve'),
)
