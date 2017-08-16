from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from django.db.models import Max
from random import randint
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Users, News, NewsSection, Comments, Logs, Captcha

import sqlite3

#disabling csrf (cross site request forgery)
@csrf_exempt

#Show Main Page
def HomePage(request):
	Sections = NewsSection.objects.order_by('id')
	MaxID = News.objects.aggregate(maxid = Max('id'))['maxid']
	LastNews = News.objects.filter(id = MaxID)
	context_dict = { 'Sections' : Sections, 'LastNews': LastNews}
	return render(request, 'Homepage.html', context_dict)

#Show All News in Specific Section
def ShowNewsSection(request, offset):	
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	posts = News.objects.filter(sectionID = offset)
	secname = NewsSection.objects.filter(id = offset)
	Sections = NewsSection.objects.order_by('id')
	context_dict = { 'posts' : posts, 'secname': secname, 'Sections': Sections}
	return render(request, 'ShowNewsSection.html', context_dict)

#Show News Detail
def ShowNewsDetail(request, offset):	
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	posts = News.objects.filter(id = offset)
	comments = Comments.objects.filter(NID = offset)
	Sections = NewsSection.objects.order_by('id')
	context_dict = { 'posts' : posts, 'comments': comments, 'Sections': Sections}
	return render(request, 'ShowNewsDetail.html', context_dict)

#Show Login Page
def Login(request):
	Sections = NewsSection.objects.order_by('id')
	random = randint(1, 9)
	context_dict = {'Sections': Sections, 'Random': random}
	return render(request, 'Login.html', context_dict)
	
#Show Contact Page
def ContactUs(request):
	Sections = NewsSection.objects.order_by('id')
	return render(request, 'ContactUs.html', {'Sections': Sections})

#Show User Profile
def Profile(request):
	Isadmin = False
	if request.method == 'POST':
        #getting values from post
		uname = request.POST.get('username')
		password = request.POST.get('password')
		llogin = timezone.now()
		
		#Check in DB for User
		conn = sqlite3.connect('NewsPortal.sqlite')
		c = conn.cursor()		
		
		c.execute('''SELECT COUNT(*) FROM NEWS_users Where username=? AND password=?''', (uname, password))
		result = c.fetchone() #retrieve the first row
		
		
		c.execute('''SELECT COUNT(*) FROM NEWS_users Where username=? AND password=? AND isadmin=?''', (uname, password, '1'))
		admin_result = c.fetchone() #retrieve the first row
		#return HttpResponse("Row Count: %d" % admin_result[0])
		conn.close()
		
		if admin_result[0] == 1:
			Isadmin = True
		
		if result[0] == 1:
			urname = request.POST.get('username')
			#set LastLogin to current timezone
			Users.objects.filter(username=urname).update(lastlogin=llogin)
			
		
			context = {
				'username': uname,
				'Is_admin': Isadmin
				}
		
			#getting our showdata template
			template = loader.get_template('profile.html')
		
			#returing the template 
			return HttpResponse(template.render(context, request))
		else:
			return render_to_response('login_error.html')
	
	else:
        #if post request is not true 
        #returing the form template 
		template = loader.get_template('login.html')
		return HttpResponse(template.render())
		
#Show User List Page
def UsersList(request):
	UserList = Users.objects.order_by('id')
	context_dict = { 'userlist' : UserList}
	return render(request, 'UsersList.html', context_dict)

#Show Section List Page
def SectionList(request):
	SectionsList = NewsSection.objects.order_by('id')
	UserList = Users.objects.order_by('id')
	context_dict = { 'Sections' : SectionsList, 'userlist' : UserList}
	return render(request, 'SectionList.html', context_dict)

#Section delete
def SectionDel(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	
	NewsSection.objects.filter(id = offset).delete()
	
	SectionsList = NewsSection.objects.order_by('id')
	UserList = Users.objects.order_by('id')
	context_dict = { 'Sections' : SectionsList, 'userlist' : UserList}
	return render(request, 'SectionList.html', context_dict)
	
#Section Add
def SectionAdd(request):
	if request.method == 'POST':
        #getting values from post
		secname = request.POST.get('secname')
		check = request.POST.get('checks')
		selecteduser = Users.objects.filter(id = check).first()
		section = NewsSection(Stitle = secname, SAdmin = selecteduser )
		section.save()
	
	SectionsList = NewsSection.objects.order_by('id')
	UserList = Users.objects.order_by('id')
	context_dict = { 'Sections' : SectionsList, 'userlist' : UserList}
	return render(request, 'SectionList.html', context_dict)
	
#Show News List Page
#Need Session
def NewsList(request):
	Sections = NewsSection.objects.order_by('id')
	allnews = News.objects.order_by('id')
	context_dict = { 'Sections' : Sections, 'allnews': allnews}
	return render(request, 'NewsList.html', context_dict)	

#Change Passwd
##Need Session
def ChangePass(request):
	Sections = NewsSection.objects.order_by('id')
	MaxID = News.objects.aggregate(maxid = Max('id'))['maxid']
	LastNews = News.objects.filter(id = MaxID)
	context_dict = { 'Sections' : Sections, 'LastNews': LastNews}
	return render(request, 'ChangePass.html', context_dict)	

#Add Comment to Post
def AddComment(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	
	if request.method == 'POST':
        #getting values from post
		commentname = request.POST.get('name')
		commenttext = request.POST.get('text')
		commentdate = timezone.now()
	
	CommentsNews = News.objects.filter(id = offset).first()	
	comment = Comments(NID = CommentsNews, name = commentname, text = commenttext, date = commentdate)
	comment.save()
	
	posts = News.objects.filter(id = offset)
	comments = Comments.objects.filter(NID = offset)
	Sections = NewsSection.objects.order_by('id')
	context_dict = { 'posts' : posts, 'comments': comments, 'Sections': Sections}
	return render(request, 'ShowNewsDetail.html', context_dict)

#Logout
def Logout(request):
	Sections = NewsSection.objects.order_by('id')
	MaxID = News.objects.aggregate(maxid = Max('id'))['maxid']
	LastNews = News.objects.filter(id = MaxID)
	context_dict = { 'Sections' : Sections, 'LastNews': LastNews}
	return render(request, 'Homepage.html', context_dict)

#Add user
def UserAdd(request):
	if request.method == 'POST':
        #getting values from post
		uname = request.POST.get('username')
		upass = request.POST.get('password')
		uemail = request.POST.get('email')
		user = Users(username = uname, password = upass, email = uemail, isadmin = 'False', )
		user.save()
		
	UserList = Users.objects.order_by('id')
	context_dict = { 'userlist' : UserList}
	return render(request, 'UsersList.html', context_dict)
	
#Delete user
def UserDel(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	
	Users.objects.filter(id = offset).delete()
	
	UserList = Users.objects.order_by('id')
	context_dict = { 'userlist' : UserList}
	return render(request, 'UsersList.html', context_dict)