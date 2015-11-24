#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from zhidao.models import *
import requests
import re
import sys
from zhidao.forms import *
from lxml import etree
from django.contrib.auth import *
from django.template.context_processors import csrf
from django import forms


def index(request):
	return render_to_response('index.html',{'user':request.user})
@csrf_exempt
def search(request):
	
	url="http://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word="+request.POST["question"]
	html = requests.get(url)
	html.encoding='gbk'

	WebSpider=spider()

	selector = etree.HTML(html.text)

	webtitle =selector.xpath('//*[@id="wgt-list"]/dl/dt/a')#title
	weblink =selector.xpath('//*[@id="wgt-list"]/dl/dt/a')#link
	webquestion =selector.xpath('//*[@id="wgt-list"]/dl/dd[@class="dd summary"]')#question
	webanswer =selector.xpath('//*[@id="wgt-list"]/dl/dd[@class="dd answer"]')#answer

	webdl =selector.xpath('//*[@id="wgt-list"]/dl')#title
	dllength=[]
	for dl in webdl:
		length = len(dl)
		dllength.append(length)
	
	for T in webtitle:
		info = T.xpath('string(.)')
		WebSpider.SpiderTitle(info)

	qNumber = 0
	for L in weblink:
		WebSpider.SpiderLink(L.attrib['href'],qNumber)
		qNumber+=1

	qNumber =0
	webqNumber = 0
	for Q in weblink:
		if dllength[qNumber] == 4:
			info = webquestion[webqNumber].xpath('string(.)')
			WebSpider.SpiderQuestion(info,qNumber)
			webqNumber+=1
		else:
			WebSpider.SpiderQuestion('',qNumber)
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
		Formalquestion = dbSpider(Q.Title,'#',Q.Description,Q.UserID.name,Q.ID)
		Aorial=answer.objects.filter(QuestionID_id=Q.ID)#获得对应问题的答案
		for item in Aorial:
			Formalanswer = Answer(item.ID,item.Content,item.UserID.name,item.is_best)
			Formalquestion.handleanswer(Formalanswer)
		dbQuestionList.append(Formalquestion)

	
	return render_to_response('search.html',{"html":WebSpider.list,"question1":dbQuestionList,"ss":dllength})
@csrf_exempt
def login(request):
	if request.method == "POST":
		loginform = LoginForm(request.POST)
		registerform = RegistrationForm()
		if loginform.is_valid():
			user = authenticate(email = loginform.cleaned_data['email'], password = loginform.cleaned_data['password'])
			if user is not None:
				if user.is_active:
					auth.login(request,user)
					return render_to_response('index.html',{'user':user})
	else:
		loginform = LoginForm()
        registerform = RegistrationForm()
	return render_to_response('login.html',{'loginform':loginform,'registerform':registerform})			
@csrf_exempt
def register(request):
	if request.method == "POST":
		registerform = RegistrationForm(request.POST)
		loginform = LoginForm()
		if  registerform.is_valid():
			user = User.objects.create_user(name = registerform.cleaned_data['username'],email = registerform.cleaned_data['email'],password = registerform.cleaned_data['password2'])
			user.save()
			return render_to_response('index.html')
	else:
		loginform = LoginForm()
		registerform = RegistrationForm()
	return render_to_response('login.html',{'loginform':loginform,'registerform':registerform})
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/index")
@csrf_exempt
def changepwd(request):
	if request.method == "POST":
		changepwdform = ChangepwdForm(request.POST)
		if changepwdform.is_valid():
			email = request.user.email
			oldpwd = changepwdform.cleaned_data['oldpassword']
			user = authenticate(email = email, password = oldpwd)

			if user is not None and user.is_active:
				newpwd = changepwdform.cleaned_data['newpassword2']
				user.set_password(newpwd)
				user.save()
				return render_to_response('index.html',{'user':user})
			else:
				return render_to_response('changepwd.html',{'changepwdform':changepwdform,'is_oldpwd_wrong':True})
	else:
		changepwdform = ChangepwdForm()
		return render_to_response('changepwd.html',{'changepwdform':changepwdform})
#def inforupdate(request):
	


