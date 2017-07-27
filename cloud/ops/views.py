from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
import pymysql
from django.core.cache import cache
import memcache
from ops.models import employee

# Create your views here.
#conn = pymysql.Connect(host='127.0.0.1',user='root', password='aixocm', database='www', port=3306, charset='utf8')
#cursor = conn.cursor()
#cursor.execute('select username, passwd from ops_employee')
#user_list = cursor.fetchall()   #获取所有员工信息，用户，密码
#cursor.close()
#conn.close()

#mc = memcache.Client(['127.0.0.1:11211'], debug=True)


def login(request):
	if request.POST:
		m = employee.objects.get(username=request.POST['username'])
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username == m.username and password == m.passwd:
				#cache.set('username', username, 3600)
				#mc.set('username', username, 3600)		
			request.session['username'] = m.username		
			request.session['isLogin'] = True		
			request.session.set_expiry(3600)
			return HttpResponseRedirect('/index/')
		else:
			return render(request, 'login.html')
	else:
		return render(request, 'login.html')


def index(request):
	user = request.session.get('username')
	islogin = request.session.get('isLogin')
    #user = cache.get('username')
	if islogin:
		return render(request, 'index.html', {'user': user})
	else:
		return HttpResponseRedirect('/login/')

def form(request):
	user = request.session.get('username')
	islogin = request.session.get('isLogin')
	if islogin:
		return render(request, 'form.html', {'user': user})
	else:
		return HttpResponseRedirect('/login/')

def compiler(request):
	user = request.session.get('username')
	islogin = request.session.get('isLogin')
	if user:
		return render(request, 'compiler.html', {'user': user})
	else:
		return HttpResponseRedirect('/login/')
