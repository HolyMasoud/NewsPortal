from django.shortcuts import render
from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.HomePage, name='HomePage'),
	url(r'^ShowNewsSection/(\d{1,2})/$', views.ShowNewsSection, name='ShowNewsSection'),
	url(r'^ShowNewsDetail/(\d{1,2})/$', views.ShowNewsDetail, name='ShowNewsDetail'),
	url(r'^Login/$', views.Login, name='Login'),
	url(r'^ContactUs/$', views.ContactUs, name='ContactUs'),
	url(r'^Profile/$', views.Profile, name='Profile'),
	url(r'^UsersList/$', views.UsersList, name='UsersList'),
	url(r'^SectionList/$', views.SectionList, name='SectionList'),
	url(r'^SectionAdd/$', views.SectionAdd, name='SectionAdd'),
	url(r'^SectionDel/(\d{1,2})/$', views.SectionDel, name='SectionDel'),	
	url(r'^NewsList/$', views.NewsList, name='NewsList'),
	url(r'^ChangePass/$', views.ChangePass, name='ChangePass'),
	url(r'^AddComment/(\d{1,2})/$', views.AddComment, name='AddComment'),
	url(r'^Logout/$', views.Logout, name='Logout'),
	url(r'^UserDel/(\d{1,2})/$', views.UserDel, name='UserDel'),
	url(r'^UserAdd/$', views.UserAdd, name='UserAdd'),
	url(r'^ChangePass/$', views.ChangePass, name='ChangePass'),
]