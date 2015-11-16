#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import requests
import re
import sys
from lxml import etree
def index(request):
	return render_to_response('index.html')
@csrf_exempt
def search(request):
	url="http://zhidao.baidu.com/search?word="+request.POST["question"]
	html = requests.get(url)
	html.encoding='gbk'
	selector = etree.HTML(html.text)
	aim =selector.xpath('//*[@id="wgt-list"]/dl[2]/dt/a/text()')	
	return render_to_response('search.html',{"html":aim[0])})
def login(request):
	return render_to_response('login.html')