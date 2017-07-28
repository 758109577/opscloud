from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
import pymysql
from django.core.cache import cache
import memcache
from ops.models import employee,compiler
import json
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

def compiler_host(request):
	user = request.session.get('username')
	islogin = request.session.get('isLogin')
	compilers = compiler.objects.all()
	compilers_list = []
	for i in compilers:
		compile_info = []
		compile_info.append(i.compile_name)
		compile_info.append(i.compile_ip)
		compile_info.append(i.create_user_id_id)
		compile_info.append(i.repertory_dir)
		compilers_list.append(compile_info)
	if user:
		return render(request, 'compiler.html', {'user': user,'compiler': compilers_list})
	else:
		return HttpResponseRedirect('/login/')


def update(request):
	if request.POST:
		compile_name = request.POST['compile_name']
		compile_ip = request.POST['compile_ip']
		repertory_dir = request.POST['repertory_dir']
		create_user_id_id = request.POST['create_user_id_id']
		obj = compiler.objects.get(create_user_id_id=create_user_id_id)
		obj.compile_name = compile_name
		obj.compile_ip = compile_ip
		obj.repertory_dir = repertory_dir
		obj.save()
		return HttpResponseRedirect('/login/')	
