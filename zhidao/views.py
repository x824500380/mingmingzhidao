#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt


def index(request):
	return render_to_response('index.html')
@csrf_exempt
def search(request):
	return render_to_response('search.html')
def login(request):
	return render_to_response('login.html')