#from django.shortcuts import render
from django.db import models
from django.utils import timezone

class Users(models.Model):
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	isadmin = models.BooleanField()
	lastlogin = models.DateTimeField(default=timezone.now)
	def __unicode__(self):
		return u'%s %s %s' % (self.username, self.password, self.email)
    
class News(models.Model):
	writerID = models.ForeignKey('Users', on_delete = models.CASCADE)
	sectionID = models.ForeignKey('NewsSection', on_delete = models.CASCADE)
	title = models.CharField(max_length=50)
	date = models.DateTimeField(auto_now=True)
	text = models.CharField(max_length=500)
	image = models.CharField(max_length=50)
	def __unicode__(self):
		return u'%s %s %s' % (self.title, self.text, self.image)

class NewsSection(models.Model):
	SAdmin = models.ForeignKey('Users', on_delete = models.CASCADE)
	Stitle = models.CharField(max_length=50)
	SLogo = models.CharField(max_length=50, default='logo.png')
	def __unicode__(self):
		return u'%s' % (self.Stitle)

class Comments(models.Model):
	NID = models.ForeignKey('News', on_delete = models.CASCADE)
	name = models.CharField(max_length=50)
	text = models.CharField(max_length=300)
	date = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return u'%s %s' % (self.name, self.text)

class Logs(models.Model):
	UID = models.ForeignKey('Users', on_delete = models.CASCADE)
	eventname = models.CharField(max_length=50)
	eventdetail = models.CharField(max_length=100)
	eventdate = models.DateTimeField()
	def __unicode__(self):
		return u'%s %s' % (self.eventname, self.eventdetail)

class Captcha(models.Model):
	Cpic = models.CharField(max_length=50)
	Cvalue = models.CharField(max_length=50)
	def __unicode__(self):
		return u'%s %s' % (self.Cpic, self.Cvalue)