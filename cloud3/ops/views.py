from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
import pymysql
from django.core.cache import cache
import memcache
from ops.models import employee,compiler,node_host,server_info
import json
import os
import subprocess
# Create your views here.
#conn = pymysql.Connect(host='127.0.0.1',user='root', password='aixocm', database='www', port=3306, charset='utf8')
#cursor = conn.cursor()
#cursor.execute('select username, passwd from ops_employee')
#user_list = cursor.fetchall()   #获取所有员工信息，用户，密码
#cursor.close()
#conn.close()

#mc = memcache.Client(['127.0.0.1:11211'], debug=True)

#################################登录配置#################################
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

#########################登录配置完毕###########################

##########################用户管理##############################
def user_manager(request):
	user = request.session.get('username')
	islogin = request.session.get('isLogin')
	if islogin:
		all_user = employee.objects.all()
		users_list = []
		for i in all_user:
			user_info = []
			user_info.append(i.id)
			user_info.append(i.username)
			user_info.append(i.deptment)
			user_info.append(i.permission)
			users_list.append(user_info)
		return render(request, 'user.html', {'user': user,'users_list': users_list})
	else:
		return HttpResponseRedirect('/login/')

def user_update(request):
	if request.POST:
		user_id = request.POST['user_id']
		username = request.POST['username']
		deptment = request.POST['deptment']
		permission = request.POST['permission']
		objs = employee.objects.all()
		for obj in objs:
			if obj.id == int(user_id):
				obj.username = username
				obj.deptment = deptment
				obj.permission = int(permission)
				obj.save()
				break
		else:
			obj = employee(id=user_id,username=username,deptment=deptment,permission=permission)
			obj.save()
	return HttpResponseRedirect("/login/")

def user_delete(request):
	if request.POST:
		user_id = request.POST['user_id']
		employee.objects.filter(id=user_id).delete()
		return HttpResponseRedirect("/login/")


##########################用户管理配置完毕#######################
def form(request):
	user = request.session.get('username')
	islogin = request.session.get('isLogin')
	if islogin:
		return render(request, 'form.html', {'user': user})
	else:
		return HttpResponseRedirect('/login/')


#################编译机配置#############################
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


def compiler_update(request):
	if request.POST:
		compile_name = request.POST['compile_name']
		compile_ip = request.POST['compile_ip']
		repertory_dir = request.POST['repertory_dir']
		create_user_id_id = request.POST['create_user_id_id']
		objs = compiler.objects.all()
		for obj in objs:
			if obj.compile_ip == compile_ip: 
				obj.compile_name = compile_name
				obj.compile_ip = compile_ip
				obj.repertory_dir = repertory_dir
				obj.create_user_id_id = create_user_id_id
				obj.save()
				break
		else:
			obj = compiler(compile_name=compile_name,compile_ip=compile_ip,repertory_dir=repertory_dir,create_user_id_id=create_user_id_id)
			obj.save()
	return HttpResponseRedirect("/login/")	

def compiler_delete(request):
	if request.POST:
		compile_ip = request.POST['compile_ip']
		compiler.objects.filter(compile_ip=compile_ip).delete()
		return HttpResponseRedirect("/login/")
		#return HttpResponse('ok')
##############################编译机配置完毕####################

############################节点主机配置##########################
def node(request):
	user = request.session.get('username')
	islogin = request.session.get('isLogin')
	node_hosts_obj = node_host.objects.all()
	nodes_list = []
	for i in node_hosts_obj:
		nodes_info = []
		nodes_info.append(i.node_name)
		nodes_info.append(i.node_ip)
		nodes_info.append(i.create_user_id_id)
		nodes_info.append(i.code_dir)
		nodes_list.append(nodes_info)
	if user:
		return render(request, 'node.html', {'user': user,'nodes': nodes_list})
	else:
		return HttpResponseRedirect('/login/')

def node_update(request):
	if request.POST:
		node_name = request.POST['node_name']
		node_ip = request.POST['node_ip']
		code_dir = request.POST['code_dir']
		create_user_id_id = request.POST['create_user_id_id']
		objs = node_host.objects.all()
		for obj in objs:
			if obj.node_ip == node_ip:
				obj.node_name = node_name
				obj.node_ip = node_ip
				obj.code_dir = code_dir
				obj.create_user_id_id = create_user_id_id
				obj.save()
				break
		else:
			obj = node_host(node_name=node_name,node_ip=node_ip,code_dir=code_dir,create_user_id_id=create_user_id_id)
			obj.save()
	return HttpResponseRedirect("/login/")


def node_delete(request):
	if request.POST:
		node_ip = request.POST['node_ip']
		node_host.objects.filter(node_ip=node_ip).delete()
		return HttpResponseRedirect("/login/")

########################节点主机配置完毕########################

#####################server配置###############################
def server(request):
	user = request.session.get('username')
	islogin = request.session.get('isLogin')
	if islogin:
		server_dic = {
				'oss对象存储':'ossServer',
				'tsa服务':'tsaServer',
				'sms短信服务':'smsServer',
				'service唯一单号':'commonServer',
				'nest-api':'apiServer',
				'nest-task':'taskServer',
				'core-server':'coreServer',
				'pay-server':'payServer',
				'bill':'billServer',
				'h5':'h5Server',
				'web':'webServer',
				'loan-server':'loanServer',
				'manager':'managerServer',
				'stat':'statisticServer',
				'jxpay-server':'jxpayServer'				
			}
		project_key = request.GET['server_name']
		project_value = server_dic[project_key]
		obj = server_info.objects.filter(application=project_value)
		obj_list = []
		for i in obj:
			temp_list = []
			temp_list.append(i.application)
			temp_list.append(i.server_ip)
			temp_list.append(i.server_port)
			temp_list.append(i.image_id)
			temp_list.append(i.container_id)
			temp_list.append(i.container_status)
			obj_list.append(temp_list)
		obj_json = json.dumps(obj_list)
		return HttpResponse(obj_json)
	else:
		return HttpResponseRedirect("/login/")

def server_app(request):
	user = request.session.get('username')
	islogin = request.session.get('isLogin')
	if islogin:
		id_json = request.GET['id']
		server_list = json.loads(id_json)
		hosts_obj = node_host.objects.all().values('node_ip')
		host_list = []
		for i in hosts_obj:
			host_list.append(i['node_ip'])
		return render(request, 'server.html', {'user':user, 'server_list': server_list,'host_list':host_list})
	else:
		return HttpResponseRedirect("/login/")

def server_add(request):
	user = request.session.get('username')
	islogin = request.session.get('isLogin')
	if islogin and request.POST:
		application = request.POST['appname']
		server_ip = request.POST['host_ip']
		port = int(request.POST['port'])
		server_info.objects.create(application=application,server_ip=server_ip,server_port=port,image_id='',container_id='',container_status='')
		return HttpResponseRedirect('/index/')
	else:
		return HttpResponseRedirect("/login/")

def server_del(request):
	user = request.session.get('username')
	islogin = request.session.get('isLogin')
	if islogin and request.POST:
		node_name = request.POST['node_name']
		node_ip = request.POST['node_ip']
		server_info.objects.filter(application=node_name,server_ip=node_ip).delete()
		return HttpResponse("ok")
	else:
		return HttpResponse("error")


def comp_mvn(request):
	user = request.session.get('username')
	islogin = request.session.get('isLogin')
	if islogin and request.POST:
		git_url = request.POST['git_url']
		p = subprocess.Popen(['/root/hyh/cloud/git_get_code.py',git_url],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		git_log = p.stdout.read()
		git_err_log = p.stderr.read()
		with open("/root/hyh/cloud/git.log",'w') as f:
			f.write(git_log)

		with open("/root/hyh/cloud/git_err.log",'w') as f:
			f.write(git_err_log)
		return HttpResponse(git_log)
	else:
		return HttpResponse(git_err_log)			

##############################server配置结束##################
