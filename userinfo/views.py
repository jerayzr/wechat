#coding=utf-8
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from datetime import datetime
import time
import urllib
import json
from pprint import pprint
from userinfo.models import UserInfo
from wechat.views import get_xml_info

def get_time(raw_time):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(raw_time))

def is_signin(func):
    def _is_signin(request, *args, **argss):
        wechat_id = request.GET.get('wechat_id', None)
        s_wechat_id = request.session.get('s_wechat_id', None)
        if not s_wechat_id:
            return HttpResponseRedirect('./signin/?wechat_id='+wechat_id)
        argss.update({'wechat_id':s_wechat_id})
        return func(request, *args, **argss)
    return _is_signin

def user_signin(request, template='signin.html'):
    wechat_id = request.GET.get('wechat_id', None)
    dicts = {}
    if request.method == 'POST':
        username = request.POST.get('username', None)
        user = UserInfo.objects.filter(wechat_id=wechat_id)
        if not user:
            user = UserInfo(wechat_id=wechat_id,
                            username = username,
                            first_signin_time = get_time(time.time()),
                            last_signin_time = get_time(time.time()))
            user.save()
        else:
            if not user[0].username == username:
                return HttpResponseRedirect('./?wechat_id='+wechat_id)
            user[0].last_signin_time = get_time(time.time())
            user[0].save()
        request.session['s_wechat_id'] = wechat_id
        request.session.set_expiry(0)
        return HttpResponseRedirect('../')
    return render_to_response(template, dicts)

@is_signin
def user_info(request, wechat_id, template='info.html'):
    user_info = UserInfo.objects.filter(wechat_id=wechat_id)
    dicts = {}
    if user_info:    
        dicts = {'user_info':user_info[0]}
    return render_to_response(template, dicts)

def oauth(request, template='userinfo.html'):
    code = request.GET.get('code', None)
    state = request.GET.get('state', None)
    return_json = urllib.urlopen('https://api.weixin.qq.com/sns/oauth2/access_token?appid=wxc4d4838cfad9a1e0&secret=7a29d16a7785eac78eb4e74190291c01&code=%s&grant_type=authorization_code'%code).read()
    json_info = json.loads(return_json)
    ErrCode = "errcode"
    if ErrCode in json_info.keys(): 
        return HttpResponse(return_json)
    access_token = json_info['access_token']
    openid = json_info['openid']
    lang = "zh_CN"
    return_user_info = urllib.urlopen('https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=%s'%(access_token, openid, lang)).read()
    json_user_info = json.loads(return_user_info)
    if ErrCode in json_user_info.keys():
        return HttpResponse(return_user_info)
    return render_to_response(template, json_user_info)
