#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from zhidao.models import question,answer,user,spider,Answer,dbSpider

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

	WebSpider=spider()

	selector = etree.HTML(html.text)

	webtitle =selector.xpath('//*[@id="wgt-list"]/dl/dt/a')#title
	weblink =selector.xpath('//*[@id="wgt-list"]/dl/dt/a')#link
	webquestion =selector.xpath('//*[@id="wgt-list"]/dl/dd[@class="dd summary"]')#question
	webanswer =selector.xpath('//*[@id="wgt-list"]/dl/dd[@class="dd answer"]')#answer

	for T in webtitle:
		info = T.xpath('string(.)')
		WebSpider.SpiderTitle(info)

	qNumber = 0
	for L in weblink:
		WebSpider.SpiderLink(L.attrib['href'],qNumber)
		qNumber+=1

	qNumber =0
	for Q in webquestion:
		info = Q.xpath('string(.)')
		WebSpider.SpiderQuestion(info,qNumber)
		qNumber+=1

	qNumber = 0
	for A in webanswer:
		info = A.xpath('string(.)')
		WebSpider.SpiderAnswer(info,qNumber)
		qNumber+=1
	qNumber = 0

	title = request.POST['question']
	question_list = question.objects.filter(Title__icontains=title)#获得数据库里的原始问题数据

	dbQuestionList=[]#存储格式化后的数据库问题
    
	for Q in question_list:
		Formalquestion = dbSpider(Q.Title,'#',Q.Description,Q.UserID.Name)
		Aorial=answer.objects.filter(QuestionID_id=Q.ID)#获得对应问题的答案
		for item in Aorial:
			Formalanswer = Answer(item.ID,item.Content,item.UserID.Name)
			Formalquestion.handleanswer(Formalanswer)
		dbQuestionList.append(Formalquestion)

	
	return render_to_response('search.html',{"html":WebSpider.list,"question1":dbQuestionList})
def login(request):
	return render_to_response('login.html')