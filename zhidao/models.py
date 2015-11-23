#coding: utf-8
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.contrib import admin

class UserManager(BaseUserManager):

    def create_user(self, name, email, password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name,
            email=UserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None):

        user = self.create_user(name, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_of_birth = models.DateField(blank = True,null = True)
    gender = models. IntegerField(default = 1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default = False)
    is_admin = models.BooleanField(default=False)
    address = models.CharField(max_length=140,blank=True, null=True)
    information = models.TextField()
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name',)


    def __unicode__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admins




class question(models.Model):
	ID = models.AutoField(primary_key = True)
	UserID = models.ForeignKey("User")
	Title = models.CharField(max_length = 100)
	KeyWords = models.CharField(max_length = 100)
	Description = models.TextField()
class answer(models.Model):
	ID = models.AutoField(primary_key = True)
	QuestionID = models.ForeignKey("question")
	Content = models.TextField()
	is_best = models.BooleanField()
	UserID = models.ForeignKey("User")

class spider:
    def __init__(self):
        self.title=''
        self.link=''
        self.question=''
        self.answer=''
        self.list=[]

    def SpiderTitle(self,title):
        self.title=title
        newspider=spider()
        newspider.title =self.title
        self.list.append(newspider)

    def SpiderLink(self,link,numb):
        self.list[numb].link=link
    def SpiderQuestion(self,question,numb):
        self.list[numb].question=question
    def SpiderAnswer(self,answer,numb):
        self.list[numb].answer=answer
class Answer:
    def __init__(self,ID,Content,Username,is_best):
        self.ID = ID
        self.Content = Content
        self.Username = Username
        self.is_best = is_best
class dbSpider:
    def __init__(self,title,link,question,username,ID):
        self.ID=ID
        self.title = title
        self.link = link
        self.question = question
        self.answers=[]
        self.bestanswer = []
        self.username = username
    def handleanswer(self,answer):
        if answer.is_best:
            self.bestanswer.append(answer)
        else:
            self.answers.append(answer)
