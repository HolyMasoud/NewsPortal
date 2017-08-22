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
# Main Page #######################################################################################
#Show Main Page
def Homepage(request):
	Sections = NewsSection.objects.order_by('id')
	MaxID = News.objects.aggregate(maxid = Max('id'))['maxid']
	LastNews = News.objects.filter(id = MaxID)
	context_dict = { 'Sections' : Sections, 'LastNews': LastNews}
	return render(request, 'Homepage.html', context_dict)

# Main NEWS Part ##################################################################################
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

# User Mgmt #######################################################################################
#Show Login Page
def Login(request):
	if request.session.has_key('username'):
		uname = request.session['username']
		
		#Log
		userx = Users.objects.filter(username = uname).first()
		log = Logs(UID = userx, eventname = "Login Success." ,eventdetail = "User Logged in Successfully.")
		log.save()
		
		return render(request, 'Profile.html', {'username': uname})
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)

#Show Login Error Page
def LoginError(request):
	Sections = NewsSection.objects.order_by('id')
	context_dict = {'Sections': Sections}
	return render(request, 'LoginError.html', context_dict)

#Show User Profile
def Profile(request):
	#IsAdmin = True
	#IsWriter = False
	if request.method == 'POST':
        #getting values from post
		uname = request.POST.get('username')
		passwd = request.POST.get('password')
		llogin = timezone.now()
		
		#Check User Exist
		ExistUser = Users.objects.filter(username = uname, password=passwd)
		if not ExistUser:
			#if user not exist
			template = loader.get_template('LoginError.html')
			return HttpResponse(template.render())
		else:
			#set LastLogin to current timezone
			Users.objects.filter(username = uname).update(lastlogin = llogin)
			user = Users.objects.filter(username = uname).get()
			request.session['username'] = user.username
			request.session['id'] = user.id
			
						
			context_dict = {'username': uname} #, 'Is_admin': IsAdmin, 'Is_writer': IsWriter
			return render(request, 'Profile.html', context_dict)
			
	
	else:
        #if post request is not true 
        #returing the form template 
		template = loader.get_template('Login.html')
		return HttpResponse(template.render())
		
#Show User List Page
def UsersList(request):
	if request.session.has_key('username'):
		uname = request.session['username']
		
		IsAdmin = Users.objects.filter(username = uname).get()
		if IsAdmin.isadmin == 1:
			UserList = Users.objects.order_by('id')
			context_dict = { 'userlist' : UserList, 'username': uname}
			return render(request, 'UsersList.html', context_dict)
		else:
			context_dict = {'username': uname}
			return render(request, 'AccessDenied.html', context_dict)
	
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)

#Add user
def UserAdd(request):
	if request.session.has_key('username'):
		uname = request.session['username']
		UID = request.session['id']
		
		if request.method == 'POST':
			#getting values from post
			uname = request.POST.get('username')
			upass = request.POST.get('password')
			uemail = request.POST.get('email')
			user = Users(username = uname, password = upass, email = uemail, isadmin = '0')
			user.save()
			
			#Log
			userx = Users.objects.filter(username = uname).first()
			log = Logs(UID = userx, eventname = "Add User." ,eventdetail = "A User Account add to system successfully.")
			log.save()
		
		UserList = Users.objects.order_by('id')
		context_dict = { 'userlist' : UserList, 'username':request.session['username']}
		return render(request, 'UsersList.html', context_dict)
	
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)
	
#Delete user
def UserDel(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	
	Users.objects.filter(id = offset).delete()
	
	UserList = Users.objects.order_by('id')
	context_dict = { 'userlist' : UserList, 'username':request.session['username']}
	return render(request, 'UsersList.html', context_dict)

#Change Passwd
def ChangePass(request):
	if request.session.has_key('username'):
		uname = request.session['username']
		UID =  request.session['id']
		
		if request.method == 'POST':
			#getting values from post
			passwd1 = request.POST.get('password1')
			passwd2 = request.POST.get('password2')
			
			if passwd1 == passwd2 and passwd1 != '':
				chpasswd = Users.objects.filter(id = UID).update(password = passwd1)
				Result = 1
				
				#Log
				userx = Users.objects.filter(username = uname).first()
				log = Logs(UID = userx, eventname = "Password Change." ,eventdetail = "User Change Password Successfully.")
				log.save()
				
			else:
				Result = 0
					
			context_dict = { 'Result': Result, 'username': request.session['username']}
			return render(request, 'ChangePass.html', context_dict)
		else:
			context_dict = {'username': request.session['username']}
			return render(request, 'ChangePass.html', context_dict)
	
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random, 'username': request.session['username']}
		return render(request, 'Login.html', context_dict)
		
	
	Sections = NewsSection.objects.order_by('id')
	MaxID = News.objects.aggregate(maxid = Max('id'))['maxid']
	LastNews = News.objects.filter(id = MaxID)
	context_dict = { 'Sections' : Sections, 'LastNews': LastNews}
	return render(request, 'ChangePass.html', context_dict)	

# News Section Mgmt ###############################################################################
#Show Section List Page
def SectionList(request):
	if request.session.has_key('username'):
		uname = request.session['username']
		
		IsAdmin = Users.objects.filter(username = uname).get()
		if IsAdmin:
			SectionsList = NewsSection.objects.order_by('id')
			UserList = Users.objects.order_by('id')
			context_dict = { 'Sections' : SectionsList, 'userlist' : UserList, 'username':request.session['username']}
			return render(request, 'SectionList.html', context_dict)
		else:
			context_dict = {'username': uname}
			return render(request, 'AccessDenied.html', context_dict)
	
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)

#Section delete
def SectionDel(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	
	if request.session.has_key('username'):
		uname = request.session['username']
	
		NewsSection.objects.filter(id = offset).delete()
		
		#Log
		userx = Users.objects.filter(username = uname).first()
		log = Logs(UID = userx, eventname = "News Section Deleted." ,eventdetail = "Administrator of System Delete a news section successfully.")
		log.save()
		
		SectionsList = NewsSection.objects.order_by('id')
		UserList = Users.objects.order_by('id')
		context_dict = { 'Sections' : SectionsList, 'userlist' : UserList, 'username':request.session['username']}
		return render(request, 'SectionList.html', context_dict)
	
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)
	
#Section Add
def SectionAdd(request):
	if request.session.has_key('username'):
		uname = request.session['username']
		
		if request.method == 'POST':
			#getting values from post
			secname = request.POST.get('secname')
			check = request.POST.get('checks')
			selecteduser = Users.objects.filter(id = check).first()
			section = NewsSection(Stitle = secname, SAdmin = selecteduser )
			section.save()
			
			#Log
			userx = Users.objects.filter(username = uname).first()
			log = Logs(UID = userx, eventname = "Add News Section." ,eventdetail = "A news Section added by Administrator.")
			log.save()
		
		SectionsList = NewsSection.objects.order_by('id')
		UserList = Users.objects.order_by('id')
		context_dict = { 'Sections' : SectionsList, 'userlist' : UserList, 'username':request.session['username']}
		return render(request, 'SectionList.html', context_dict)
	
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)

# News Mgmt #######################################################################################
#Show News List Page
def NewsList(request):
	if request.session.has_key('username'):
		uname = request.session['username']
		UID = request.session['id']
		
		IsAdmin = NewsSection.objects.filter(SAdmin = UID).first()
		if IsAdmin:
			Sections = NewsSection.objects.filter(SAdmin = UID).all()
			allnews = News.objects.filter(writerID = UID).all()
			context_dict = { 'allnews': allnews, 'username':request.session['username'], 'Sections': Sections}
			return render(request, 'NewsList.html', context_dict)	
		else:
			context_dict = {'username': uname, 'username':request.session['username']}
			return render(request, 'AccessDenied.html', context_dict)
	
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)

#Add News
def NewsAdd(request):
	if request.session.has_key('username'):
		uname = request.session['username']
		UID = request.session['id']
		
		if request.method == 'POST':
        #getting values from post
			newstitle = request.POST.get('newstitle')
			newstext = request.POST.get('newstext')
			check = request.POST.get('checks')
			selectedsection = NewsSection.objects.filter(id = check).first()
			user = Users.objects.filter(id = UID).first()
			news = News(title = newstitle, text = newstext, writerID = user, sectionID = selectedsection )
			news.save()
			
			#Log
			userx = Users.objects.filter(username = uname).first()
			log = Logs(UID = userx, eventname = "Add News." ,eventdetail = "A news added by Users.")
			log.save()
		
			IsAdmin = NewsSection.objects.filter(SAdmin = UID).first()
			if IsAdmin:
				Sections = NewsSection.objects.filter(SAdmin = UID).all()
				allnews = News.objects.filter(writerID = UID).all()
				context_dict = { 'allnews': allnews, 'username':request.session['username'], 'Sections': Sections}
				return render(request, 'NewsList.html', context_dict)	
			else:
				context_dict = {'username': uname, 'username':request.session['username']}
				return render(request, 'AccessDenied.html', context_dict)
	
	
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)
	
#Delete NEWS
def NewsDel(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	
	if request.session.has_key('username'):
		uname = request.session['username']
		
		News.objects.filter(id = offset).delete()
		
		#Log
		userx = Users.objects.filter(username = uname).first()
		log = Logs(UID = userx, eventname = "Delete News." ,eventdetail = "A news Deleted by Users.")
		log.save()
		
		UID = request.session['id']
		IsAdmin = NewsSection.objects.filter(SAdmin = UID).first()
		if IsAdmin:
			Sections = NewsSection.objects.filter(SAdmin = UID).all()
			allnews = News.objects.filter(writerID = UID).all()
			context_dict = { 'allnews': allnews, 'username':request.session['username'], 'Sections': Sections}
			return render(request, 'NewsList.html', context_dict)	
		else:
			context_dict = {'username': uname, 'username':request.session['username']}
			return render(request, 'AccessDenied.html', context_dict)
		
		
	
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)

#Edit NEWS
def NewsEdit(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
		
	if request.session.has_key('username'):
		uname = request.session['username']
		UID = request.session['id']
		
		news = News.objects.filter(id = offset)
		IsAdmin = News.objects.filter(writerID = UID).first()
		if IsAdmin:
			context_dict = { 'news': news, 'username':request.session['username']}
			return render(request, 'NewsEdit.html', context_dict)	
		else:
			context_dict = {'username': uname, 'username':request.session['username']}
			return render(request, 'AccessDenied.html', context_dict)
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)

#Edit NEWS Final
def NewsEditFinal(request):
	if request.session.has_key('username'):
		uname = request.session['username']
		UID = request.session['id']
		
		if request.method == 'POST':
        #getting values from post
			newstitle = request.POST.get('newstitle')
			newstext = request.POST.get('newstext')
			newsid = request.POST.get('ID')
			
			IsAdmin = News.objects.filter(id = newsid, writerID = UID).first()
			if IsAdmin:
				newsupdate = News.objects.filter(id = newsid).update(title = newstitle, text = newstext)
				newsupdate.save()
				
				#Log
				userx = Users.objects.filter(username = uname).first()
				log = Logs(UID = userx, eventname = "Edit News." ,eventdetail = "A news Edited by Users.")
				log.save()
				
				Sections = NewsSection.objects.filter(SAdmin = UID).all()
				allnews = News.objects.filter(writerID = UID).all()
				context_dict = { 'allnews': allnews, 'username':request.session['username'], 'Sections': Sections}
				return render(request, 'NewsList.html', context_dict)	
			else:
				context_dict = {'username': uname, 'username':request.session['username']}
				return render(request, 'AccessDenied.html', context_dict)
		
		else:
			#nothing
			raise Http404()
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)

# Comment Mgmt ####################################################################################
#Show Comments List Page
def CommentsList(request):
	if request.session.has_key('username'):
		uname = request.session['username']
		UID = request.session['id']
		
		IsAdmin = NewsSection.objects.filter(SAdmin = UID).first()
		if IsAdmin:
			allcomments = Comments.objects.filter(NID = News.objects.filter(writerID = UID).all())
				
			context_dict = {'username':request.session['username'], 'allcomments': allcomments}
			return render(request, 'CommentsList.html', context_dict)	
		else:
			context_dict = {'username': uname, 'username':request.session['username']}
			return render(request, 'AccessDenied.html', context_dict)
	
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)

#Delete Comment
def CommentsDel(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	
	if request.session.has_key('username'):
		uname = request.session['username']
		UID = request.session['id']
		IsAdmin = NewsSection.objects.filter(SAdmin = UID).first()
		
		selectedcomment = Comments.objects.filter(id = offset).first()
		snews = News.objects.filter(writerID = UID).first()
		
		if selectedcomment.NID == snews:
			scomment = Comments.objects.filter(id = offset).delete()
			
			#Log
			userx = Users.objects.filter(username = uname).first()
			log = Logs(UID = userx, eventname = "Delete Comment." ,eventdetail = "A Comment Deleted by Users.")
			log.save()
			
			if IsAdmin:
				allcomments = Comments.objects.filter(NID = News.objects.filter(writerID = UID).all())
				context_dict = {'username':request.session['username'], 'allcomments': allcomments}
				return render(request, 'CommentsList.html', context_dict)	
			
		else:
			context_dict = {'username': uname, 'username':request.session['username']}
			return render(request, 'AccessDenied.html', context_dict)
	
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)

#Add Comment
def CommentsAdd(request, offset):
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

# Other ###########################################################################################
#Logout
def Logout(request):
	try:
		del request.session['username']
		#Log
		userx = Users.objects.filter(username = uname).first()
		log = Logs(UID = userx, eventname = "User Logout." ,eventdetail = "A User Logout From System.")
		log.save()
		
	except:
		pass
	Sections = NewsSection.objects.order_by('id')
	MaxID = News.objects.aggregate(maxid = Max('id'))['maxid']
	LastNews = News.objects.filter(id = MaxID)
	context_dict = { 'Sections' : Sections, 'LastNews': LastNews}
	return render(request, 'Homepage.html', context_dict)

#Show Contact Page
def ContactUs(request):
	Sections = NewsSection.objects.order_by('id')
	return render(request, 'ContactUs.html', {'Sections': Sections})

#Show Log List
def LogsList(request):
	if request.session.has_key('username'):
		uname = request.session['username']
		
		IsAdmin = Users.objects.filter(username = uname).get()
		if IsAdmin.isadmin == 1:
			events = Logs.objects.order_by('-id')
			UserList = Users.objects.order_by('id')
			context_dict = {'events': events, 'UserList': UserList, 'username': uname}
			return render(request, 'LogsList.html', context_dict)
		else:
			context_dict = {'username': uname}
			return render(request, 'AccessDenied.html', context_dict)
	
	else:
		Sections = NewsSection.objects.order_by('id')
		random = randint(1, 9)
		context_dict = {'Sections': Sections, 'Random': random}
		return render(request, 'Login.html', context_dict)
	