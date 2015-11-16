#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import requests
import re
import sys
from lxml import etree

def xmlatital(lis,title):

	dis = {
	"title":title,
	"link":'',
	"question":'',
	"answer":'',
	}
	lis.append(dis)

def xmlalink(lis,link,numb):
	lis[numb]["link"] =link
def xmlaques(lis,question,numb):
	lis[numb]["question"]=question
def xmlaansw(lis,answer,numb):
	lis[numb]["answer"]=answer
 

def index(request):
	return render_to_response('index.html')
@csrf_exempt
def search(request):
	url="http://zhidao.baidu.com/search?word="+request.POST["question"]
	html = requests.get(url)
	html.encoding='gbk'
	word =[]
	selector = etree.HTML(html.text)
	aaim =selector.xpath('//*[@id="wgt-list"]/dl/dt/a')#title
	link =selector.xpath('//*[@id="wgt-list"]/dl/dt/a')#link
	question =selector.xpath('//*[@id="wgt-list"]/dl/dd[@class="dd summary"]')#question
	answer =selector.xpath('//*[@id="wgt-list"]/dl/dd[@class="dd answer"]')#answer
	for a in aaim:
		info = a.xpath('string(.)')
		xmlatital(word,info)
	qNumber = 0
	for l in link:
		xmlalink(word,l.attrib['href'],qNumber)
		qNumber+=1
	qNumber =0
	for q in question:
		info = q.xpath('string(.)')
		xmlaques(word,info,qNumber)
		qNumber+=1
	qNumber = 0
	for q in answer:
		info = q.xpath('string(.)')
		xmlaansw(word,info,qNumber)
		qNumber+=1
	qNumber = 0
	return render_to_response('search.html',{"html":word})
def login(request):
	return render_to_response('login.html')