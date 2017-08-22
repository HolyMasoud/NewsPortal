from django.shortcuts import render
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.Homepage, name='Homepage'),
	url(r'^ShowNewsSection/(\d{1,2})/$', views.ShowNewsSection, name='ShowNewsSection'),
	url(r'^ShowNewsDetail/(\d{1,2})/$', views.ShowNewsDetail, name='ShowNewsDetail'),
	
	url(r'^Login/$', views.Login, name='Login'),
	url(r'^LoginError/$', views.LoginError, name='LoginError'),
	url(r'^Profile/$', views.Profile, name='Profile'),
	
	url(r'^UsersList/$', views.UsersList, name='UsersList'),
	url(r'^UserDel/(\d{1,2})/$', views.UserDel, name='UserDel'),
	url(r'^UserAdd/$', views.UserAdd, name='UserAdd'),
	
	url(r'^SectionList/$', views.SectionList, name='SectionList'),
	url(r'^SectionAdd/$', views.SectionAdd, name='SectionAdd'),
	url(r'^SectionDel/(\d{1,2})/$', views.SectionDel, name='SectionDel'),	
	
	url(r'^NewsList/$', views.NewsList, name='NewsList'),
	url(r'^NewsEdit/(\d{1,2})/$', views.NewsEdit, name='NewsEdit'),
	url(r'^NewsEditFinal/$', views.NewsEditFinal, name='NewsEditFinal'),
	url(r'^NewsDel/(\d{1,2})/$', views.NewsDel, name='NewsDel'),
	url(r'^NewsAdd/$', views.NewsAdd, name='NewsAdd'),
	
	url(r'^CommentsList/$', views.CommentsList, name='CommentsList'),
	url(r'^CommentsAdd/(\d{1,2})/$', views.CommentsAdd, name='CommentsAdd'),
	url(r'^CommentsDel/(\d{1,5})/$', views.CommentsDel, name='CommentsDel'),
	
	url(r'^Logout/$', views.Logout, name='Logout'),
	url(r'^ChangePass/$', views.ChangePass, name='ChangePass'),
	url(r'^LogsList/$', views.LogsList, name='LogsList'),
	url(r'^ContactUs/$', views.ContactUs, name='ContactUs'),
]