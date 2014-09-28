#coding=utf-8
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from datetime import datetime
from userinfo.models import UserInfo
from wechat.views import get_xml_info
def is_signin(func):
    def _is_signin(request, *args, **argss):
        wechat_id = request.session.get('wechat_id', None)
        if not wechat_id:
            return HttpResponseRedirect('./signin/?wechat_id='+wechat_id)
        argess.update({'wechat_id':wechat_id})
        return func(request, *args, **argss)
    return _is_signin

def user_signin(request, template='signin.html'):
    wechat_id = request.GET.get('wechat_id', None)
    dicts = {}
    if request.method == 'POST':
        username = request.POST.get('username', None)
        user = UserInfo.objects.filter(wechat_id=wechat_id, username=username)
        if not user:
            user = UserInfo(wechat_id=wechat_id,
                            username = username,
                            first_signin_time = datetime.now(),
                            last_signin_time = datetime.now())
            user.save()
       else:
            user.last_signin_time = datetime.now()
            user.save()
       request.session['wechat_id'] = wechat_id
       request.session.set_expiry(0)
    return render_to_response(template, dicts)

@is_signin
def user_info(request, template='info.html'):
    dicts = {}
    return render_to_response(template, dicts)
