#coding=utf-8
from django.db import models

class UserInfo(models.Model):
    '''用户信息表'''
    wechat_id = models.CharField(max_length=64, null=True)  
    '''微信id，每个用户唯一''' 
    username = models.CharField(max_length=64, null=True)
    '''用户名，用户第一次登录时输入'''
    first_signin_time = models.DateTimeField(null=True)
    '''用户第一次登录的时间'''
    last_signin_time = models.DateTimeField(null=True)
    '''用户的最近一次登录时间，可以根据此时间判断用户下一次的登录时间'''
     
