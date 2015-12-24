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
from django.contrib.auth.decorators import login_required
from zhidao.forms import *
from lxml import etree
from django.contrib.auth import *
from django.template.context_processors import csrf
from django import forms
from django.http import HttpResponseRedirect
import urllib
def webspider(WebSpider,url):
	html = requests.get(url)
	html.encoding='gbk'
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
		if dllength[qNumber] == 4 and len(webquestion)>webqNumber:
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
def messagenumber(user):
	if user.is_authenticated():
		count = 0
		allmessage = user.To_id.all()
		for item in allmessage:
			if not item.is_view:
				count += 1
		return count
	else:
		return 0
def index(request):
	return render_to_response('index.html',{'user':request.user,'messages':messagenumber(request.user)})
@csrf_exempt
def pre_search(request,key):
	question=request.POST['question']
	url='/search/'+question+'/1'
	return HttpResponseRedirect(url)
def search(request,key,wd):
	
	reload(sys)

	sys.setdefaultencoding('utf8')
	
	postquestio=wd
	postquestion=urllib.quote(postquestio.decode('utf8','ignore').encode('gbk','ignore'))
	#postquestion2=postquestion.decode(encoding='gbk',errors='strict')
	url="http://zhidao.baidu.com/search?lm=0&rn=10&pn="+str(int(key)*10)+"&fr=search&ie=gbk&word="+postquestion

	spiderlist=[]
	
	WebSpider=spider()
	webspider(WebSpider,url)

	title = wd
	question_list = question.objects.filter(Title__icontains=title)#获得数据库里的原始问题数据

	dbQuestionList=[]#存储格式化后的数据库问题
    
	for Q in question_list:
		Formalquestion = dbSpider(Q.Title,'#',Q.Description,Q.UserID.id,Q.ID)
		Aorial=answer.objects.filter(QuestionID_id=Q.ID)#获得对应问题的答案
		for item in Aorial:
			exquestions = ExQuestion.objects.filter(AnswerID = item)
			Formalanswer = Answer(item.ID,item.Content,item.UserID.name,item.is_best,exquestions)
			Formalquestion.handleanswer(Formalanswer)
		dbQuestionList.append(Formalquestion)
	keynext=int(key)+1
	keyformer=int(key)-1
	return render_to_response('search.html',{"keyformer":keyformer,'messages':messagenumber(request.user),"keynext":keynext,"url":url,"key":key,"wd":wd,"char":postquestion,"q":wd,"html":WebSpider.list,"question1":dbQuestionList,"user":request.user})
@csrf_exempt
def login(request):
	if request.method == "GET":
		request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
		loginform = LoginForm()
        registerform = RegistrationForm()
	if request.method == "POST":
		loginform = LoginForm(request.POST)
		registerform = RegistrationForm()
		if loginform.is_valid():
			user = authenticate(email = loginform.cleaned_data['email'], password = loginform.cleaned_data['password'])
			if user is not None:
				if user.is_active:
					auth.login(request,user)
					return HttpResponseRedirect(request.session['login_from'])
		else:
			return render_to_response('login.html',{'loginform':loginform,'registerform':registerform})	
	return render_to_response('login.html',{'loginform':loginform,'registerform':registerform})			
@csrf_exempt
def register(request):
	if request.method == "POST":
		registerform = RegistrationForm(request.POST)
		loginform = LoginForm()
		if  registerform.is_valid():
			user = User.objects.create_user(name = registerform.cleaned_data['username'],email = registerform.cleaned_data['email'],password = registerform.cleaned_data['password2'])
			user.save()
			newmessage = Message(To_id = user.id,
				From_id = None,
				QuestionID = None,
				AnswerID = None,
				MessageType = 0)
			newmessage.save()
			return HttpResponseRedirect('../index')
	else:
		loginform = LoginForm()
		registerform = RegistrationForm()
	return render_to_response('login.html',{'loginform':loginform,'registerform':registerform})
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('../index')
def usercenter(request):
	return render_to_response('information.html',{'user':request.user,'messages':messagenumber(request.user)})
@csrf_exempt
@login_required(login_url='/login')
def changepwd(request):
	if request.method == "POST":
		form = ChangepwdForm(user = request.user, data = request.POST)
		if form.is_valid():
			user = request.user
			user.set_password(form.cleaned_data['newpassword2'])
			user.save()
		return HttpResponseRedirect("/information")
	else:
		form = ChangepwdForm(user = request.user)
	return render_to_response('changepwd.html',{'changepwdform':form,'user':request.user,'messages':messagenumber(request.user)})
@csrf_exempt
@login_required(login_url='/login')
def inforupdate(request):
	if request.method == "POST":
		form = InformationForm(request.POST)
		if form.is_valid():
			request.user.gender = form.cleaned_data['gender']
			request.user.date_of_birth = form.cleaned_data['birthday']
			request.user.address = form.cleaned_data['address']
			request.user.information = form.cleaned_data['information']
			request.user.save()
			return HttpResponseRedirect("../usercenter/information")
	else:
		form = InformationForm(initial = {'gender':request.user.gender,
			'birthday':request.user.date_of_birth,
			'address':request.user.address,
			'information':request.user.information})
	return render_to_response('inforupdate.html',{'informationform':form,'user':request.user,'messages':messagenumber(request.user)})
@csrf_exempt
@login_required(login_url='/login')
def putquestion(request):
	if request.method == "POST":
		form = QuestionForm(request.POST,auto_id = True)
		if form.is_valid():
			questionID = form.save(request.user)
			url = '/'+str(questionID)+'/'+str(request.user.id)+'/detail'
			return HttpResponseRedirect(url)
	else:
		form = QuestionForm()
	return render_to_response('put_question.html',{"user":request.user,'form':form,'messages':messagenumber(request.user)})
@csrf_exempt
def questiondetail(request,questionID,userID):
	user = User.objects.get(id = userID)
	questiontemp = question.objects.get(ID = questionID)
	try:
		bestanswer=answer.objects.get(is_best=1,QuestionID_id = questionID)
		bestuser=User.objects.get(id = bestanswer.UserID_id)
		bestanswer_ex = ExQuestion.objects.filter(AnswerID = bestanswer)
	except:
		bestanswer = []
		bestuser = []
		bestanswer_ex = []
	try:
		otheranswer=answer.objects.filter(is_best=0,QuestionID_id = questionID)
		answerlist = []
		for item in otheranswer:
			exquestions = ExQuestion.objects.filter(AnswerID = item)
			answertemp = Answer(item.ID,item.Content,item.UserID.name,item.is_best,exquestions)
			answerlist.append(answertemp)
	except:
		answerlist = []
	answerform = AnswerForm()
	return render_to_response('questiondetail.html',{'form':answerform,'messages':messagenumber(request.user),"user":request.user,
		"bestanswer":bestanswer,"bestuser":bestuser,"bestanswer_ex":bestanswer_ex,
		"question":questiontemp,"questionuser":user,
		"answerlist":answerlist})
@csrf_exempt
@login_required(login_url='/login')
def putanswer(request,questionID):
	if request.method == "POST":
		form = AnswerForm(request.POST,auto_id = True)
		if form.is_valid():
			questiontemp = question.objects.get(ID = questionID)
			answertemp = form.save(request.user,questiontemp)
			newmessage = Message(To_id = questiontemp.UserID_id,
				From_id = answertemp.UserID_id,
				QuestionID = questiontemp,
				AnswerID = answertemp,
				MessageType = 1)
			newmessage.save()
			url = '/'+str(questionID)+'/'+str(questiontemp.UserID_id)+'/detail'
			return HttpResponseRedirect(url)
	else:
		form = AnswerForm()
	return render_to_response('questiondetail.html',{'form':form,'messages':messagenumber(request.user)})
def myquestions(request):
	questionlist = question.objects.filter(UserID = request.user)
	return render_to_response('myquestions.html',{'questionlist':questionlist,'user':request.user,'messages':messagenumber(request.user)})
def myanswers(request):
	answerlist = answer.objects.filter(UserID = request.user)
	return render_to_response('myanswers.html',{'answerlist':answerlist,'user':request.user,'messages':messagenumber(request.user)})
@csrf_exempt
@login_required(login_url='/login')
def isbestanswer(request,answerID):
	bestanswer = answer.objects.get(ID = answerID)
	bestanswer.is_best = True
	bestanswer.save()
	questiontemp = bestanswer.QuestionID
	questionID = bestanswer.QuestionID_id
	newmessage = Message(To_id = bestanswer.UserID_id,
				From_id = questiontemp.UserID_id,
				QuestionID = questiontemp,
				AnswerID = bestanswer,
				MessageType = 2)
	newmessage.save()
	url = '/'+str(questionID)+'/'+str(questiontemp.UserID_id)+'/detail'
	return HttpResponseRedirect(url)
@csrf_exempt
@login_required(login_url='/login')
def messagelist(request):
	allmessage = request.user.To_id.all()
	unreadmessage = Message.objects.filter(To_id = request.user.id,is_view = False)
	return render_to_response('messagecenter.html',{'allmessage':allmessage,'unreadmessage':unreadmessage,'user':request.user,'unreadnumber':messagenumber(request.user)})
def viewmessage(request,messageID):
	message = Message.objects.get(ID = messageID)
	message.is_view = True
	message.save()
	if message.MessageType == 0:
		url = '/index'
	else:
		url = '/'+str(message.QuestionID_id)+'/'+str(message.QuestionID.UserID_id)+'/detail'
	return HttpResponseRedirect(url)
def setmessage(request,messageID):
	message = Message.objects.get(ID = messageID)
	message.is_view = True
	message.save()
	return HttpResponseRedirect('/message/list')
def setallmessage(request):
    Message.objects.filter(is_view = False).update(is_view = True)
    return HttpResponseRedirect('/message/list')
def deletemessage(request,messageID):
	message = Message.objects.get(ID = messageID)
	message.delete()
	return HttpResponseRedirect('/message/list')
def deleteallmessage(request):
	messages = Message.objects.all()
	messages.delete()
	return HttpResponseRedirect('/message/list')
def timetree(request):
	questionlist = question.objects.filter(UserID = request.user)
	answerlist = answer.objects.filter(UserID = request.user)
	timelist = timtree()

	for quest in questionlist:
		timelist.addnew(quest)
		
	for answ in answerlist:
		timelist.addnew(answ)
	timelist.getdic()
	return render_to_response('timetree.html',{'timelist':timelist,'user':request.user,'messages':messagenumber(request.user)})
@csrf_exempt
@login_required(login_url='/login')
def exquestion(request,answerID):
	if request.method == "POST":
		description = request.POST['exquestion']
		answertemp = answer.objects.get(ID = answerID)
		newexquestion = ExQuestion(Description = description,
			UserID = request.user,
			AnswerID = answertemp)
		newexquestion.save()
		newmessage = Message(To_id = answertemp.UserID_id,
			From_id = answertemp.QuestionID.UserID_id,
			QuestionID = answertemp.QuestionID,
			AnswerID = answertemp,
			MessageType = 3)
		newmessage.save()
		url = '/'+str(answertemp.QuestionID_id)+'/'+str(answertemp.QuestionID.UserID_id)+'/detail'
		return HttpResponseRedirect(url)
	