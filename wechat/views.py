#coding=utf-8
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.encoding import smart_str
import hashlib
from xml.etree import ElementTree as etree

def get_reply_xml(phrase_xml_info):
    (ToUserName, 
     FromUserName, 
     CreateTime, 
     MsgType, 
     Content, 
     MsgId) = phrase_xml_info
    #reply_info = u'欢迎使用衣食住行小助手!<a href="http://42.121.57.227/userinfo/?wechat_id=%s">请点击此处查看个人信息</a>!<a href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=gh_93a5f52f82c0&redirect_uri=http%3A%2F%2F42.121.57.227%2Foauth.html&response_type=code&scope=snsapi_userinfo&state=fuck#wechat_redirect">点击此处进行oauth认证</a>'%FromUserName
    #reply_info = u'欢迎使用衣食住行小助手!<a href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=gh_93a5f52f82c0&redirect_uri=http%3A%2F%2Fwww.1wwy.com%2Foauth.html&response_type=code&scope=snsapi_userinfo&state=fuck#wechat_redirect">点击此处进行oauth认证</a>'
    reply_info = u'欢迎Jeray的微信公众平台测试号!<a href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxc4d4838cfad9a1e0&redirect_uri=http%3A%2F%2F42.121.57.227%2Foauth.html&response_type=code&scope=snsapi_userinfo&state=test_oauth#wechat_redirect">点击此处进行oauth认证</a>'
    reply_xml = '''<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml>'''%(FromUserName, ToUserName, CreateTime, reply_info)
    return reply_xml

def get_xml_info(xml_info):
    xmlstr = smart_str(xml_info)
    xml = etree.fromstring(xmlstr)

    ToUserName = xml.find('ToUserName').text
    FromUserName = xml.find('FromUserName').text
    CreateTime = xml.find('CreateTime').text
    MsgType = xml.find('MsgType').text
    Content = xml.find('Content').text
    MsgId = xml.find('MsgId').text
    return (ToUserName, FromUserName, CreateTime, MsgType, Content, MsgId)

def wechat(request):
    if request.method == 'GET':
        response = HttpResponse(authentication(request))
        return response
    phrase_xml_info = get_xml_info(request.body)
    reply_xml = get_reply_xml(phrase_xml_info)
    return HttpResponse(reply_xml)

def authentication(request):
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    token = "yishizhuxingxiaozhushou"

    tmplist = [token,timestamp,nonce]
    tmplist.sort()
    tmpstr = "%s%s%s"%tuple(tmplist)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echostr
    else:
        return None
