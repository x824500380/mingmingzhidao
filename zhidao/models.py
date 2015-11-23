from django.db import models
from django.contrib import admin

# Create your models here.
class user(models.Model):
	Name = models.CharField(max_length = 30,unique = "True")
	ID = models.AutoField(primary_key = True)
	Gender = models.BooleanField(choices = (('F','Female'),('M','Male')))
	Birthday = models.DateField()
	Email = models.EmailField(max_length = 100)
	Passwords = models.CharField(max_length = 30)

class question(models.Model):
	ID = models.AutoField(primary_key = True)
	UserID = models.ForeignKey("user")
	Title = models.CharField(max_length = 100)
	KeyWords = models.CharField(max_length = 100)
	Description = models.TextField()
class answer(models.Model):
	ID = models.AutoField(primary_key = True)
	QuestionID = models.ForeignKey("question")
	Content = models.TextField()
	is_best = models.BooleanField()
	UserID = models.ForeignKey("user")



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


