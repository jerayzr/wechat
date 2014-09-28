#coding=utf-8
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse

def user_judge(request):
    return HttpResponse(0)

def user_signin(request):
    return HttpResponse(1)

def user_info(request):
    return HttpReponse(2)
