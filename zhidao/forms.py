#coding: utf-8
#用户注册
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from zhidao.models import *
import requests
import re
import sys

from zhidao.forms import *
from django.contrib.auth import authenticate

from django.core.exceptions import *

class RegistrationForm(forms.Form):
    username = forms.CharField(label=u"用户名",max_length=30,widget=forms.TextInput(
        attrs={'class':'input','placeholder': u'用户名', 'required': ''}
    ),
)
    email = forms.EmailField(label=u'Email', max_length=100, widget=forms.TextInput(
        attrs={ 'class':'input','placeholder': u'Email', 'required': ''}
    ),
)
    password1 = forms.CharField(label=u'密码',widget=forms.PasswordInput(
        attrs={'class':'input','placeholder': u'密码', 'required': ''}
    ),
)
    password2 = forms.CharField(label=u'密码(重复)',widget=forms.PasswordInput(
        attrs={ 'class':'input','placeholder': u'重复密码', 'required': ''}
    )
)
    def clean_username(self):
        '''验证用户输入的用户名的合法性'''
        username = self.cleaned_data['username']    
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('用户名中只能包含字母、数字和下划线')
        try:
            User.objects.get(name=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('用户名已存在！')
    
    def clean_email(self):
        '''验证输入的电子邮件是否合法'''
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('该邮箱已注册！')
    
    def clean_password2(self):
        '''验证用户两次输入的密码一致性'''
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('两次输入的密码不匹配')
class LoginForm(forms.Form):
    email = forms.EmailField(label=u'邮箱',max_length=100,widget=forms.TextInput(
        attrs={'class':'input','placeholder': u'邮箱', 'required': ''}
    ),
)
    password = forms.CharField(label=u'密码',widget=forms.PasswordInput(
        attrs={'class':'input','required': '','placeholder': u'密码'}
    ),
)
    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not User.objects.filter(email = email).exists():
            raise forms.ValidationError(u'该用户不存在')
        user_cache = authenticate(email = email,password = password)
        if user_cache is None:
            raise forms.ValidationError(u'密码错误')
        return self.cleaned_data
class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(label=u'原密码',widget=forms.PasswordInput(
        attrs={'class':'form-control','required': ''}
    ),
)
    newpassword1 = forms.CharField(label=u'新密码',widget=forms.PasswordInput(
        attrs={'class':'form-control','required': ''}
    ),
)
    newpassword2 = forms.CharField(label=u'确认密码',widget=forms.PasswordInput(
        attrs={'class':'form-control','required': ''}
    ),
)
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangepwdForm, self).__init__(*args, **kwargs)
    def clean(self):
        oldpassword = self.cleaned_data.get('oldpassword')
        newpassword1 = self.cleaned_data.get('newpassword1')
        newpassword2 = self.cleaned_data.get('newpassword2')

        if not self.user.check_password(oldpassword):
            raise forms.ValidationError(u'原密码错误')
        if newpassword1 and newpassword2:
            if newpassword2 != newpassword1:
                raise forms.ValidationError(u'两次输入的密码不匹配')
        return  self.cleaned_data

class InformationForm(forms.Form):
    SEX_CHOICES = (
    ('0','男'),
    ('1','女'),
)
    gender = forms.ChoiceField(label=u"性别",required=False,choices=SEX_CHOICES,error_messages={'invalid':u'请您正确选择下拉框'})
    birthday = forms.DateField(label=u"生日",required=False,input_formats=['%Y-%m-%d',],error_messages={'invalid':u'请输入正确格式的日期2015-01-10'})
    address = forms.CharField(label=u"地址",required=False,max_length=100,widget=forms.TextInput(
        attrs={'placeholder': u'地址'}
    ),
)
    information = forms.CharField(label=u"个人简介",required=False,max_length=400,widget=forms.Textarea(
        attrs={'placeholder': u'个人简介', }
    ),
)

class QuestionForm(forms.Form):
    title = forms.CharField(label = u"题目",error_messages={'invalid':u'问题题目不能空白'},max_length = 100)
    description = forms.CharField(label = u"详细描述", required = False,max_length = 400,widget = forms.Textarea())

    def save(self,user):
        newquestion = question(Title = self.cleaned_data['title'],
            Description = self.cleaned_data['description'],
            UserID  = user)
        newquestion.save()
        return newquestion.ID
class AnswerForm(forms.Form):
    content = forms.CharField(required = False,max_length = 400,widget = forms.Textarea(
        attrs = {'placeholder':u'你的意见呢？','class':'content'}),
    )

    def save(self,user,question):
        newanswer = answer(Content = self.cleaned_data['content'],
            UserID = user,
            QuestionID = question,
            is_best = False)
        newanswer.save()
        return newanswer.ID