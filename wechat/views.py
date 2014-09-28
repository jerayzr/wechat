#coding=utf-8
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
import hashlib


def wechat(request):
    if request.method=='GET':
        response=HttpResponse(authentication(request))
        return response

def authentication(request):
    signature=request.GET.get('signature',None)
    timestamp=request.GET.get('timestamp',None)
    nonce=request.GET.get('nonce',None)
    echostr=request.GET.get('echostr',None)
    print 1111111,signature,timestamp,nonce,echostr
    token="yishizhuxingxiaozhushou"

    tmplist=[token,timestamp,nonce]
    tmplist.sort()
    tmpstr="%s%s%s"%tuple(tmplist)
    tmpstr=hashlib.sha1(tmpstr).hexdigest()
    print 222222,tmpstr,signature,echostr
    if tmpstr==signature:
        print 99999999
        return echostr
    else:
        return None
