#!/usr/bin/python
# --*-- coding:utf-8 --*--
#编译代码, 包含克隆代码，mvn编译打包代码
import sys,os
import time
import subprocess
import shutil
import hashlib

code_dir = "/data/code/project_git"	#仓库位置
all_app_dir = "/data/code/project"	#所有应用位置
os.chdir(code_dir)	#进入仓库目录
git_url = sys.argv[1]	#git远程仓库
app_name = sys.argv[2]	#应用名
app_dir = all_app_dir + '/' + app_name	#应用目录
project_name = git_url.split('/')[1].split('.')[0]	#获取项目名
project_dir = code_dir + '/' + project_name	#拼接项目目录
src_dir = project_dir + '/' + app_name + '/target/' + app_name	#编译生成的app路径

########生成随机字符串#######
def create_md5():
	m=hashlib.md5()
	m.update(bytes(str(time.time()),encoding='utf-8'))
	return m.hexdigest()
rad = create_md5()[0:6] 
t = time.strftime("%Y%m%d-%H-%M",time.localtime(time.time()))
img_name = app_name + '_' + t + '_' + rad
###########生成字符串结束###########

############拉取代码####################
def get_code():
	is_exist_project = os.path.isdir(project_dir)	#判断项目目录是否存在,存在返回true,否则返回false
	if is_exist_project:
		os.chdir(project_dir)
		p = subprocess.Popen('git checkout master && git pull origin master',bufsize=1,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		p.wait()
		status_code = p.returncode  #git clone状态码，0表示克隆成功
		git_out = p.stdout.read().decode('utf-8')
		git_err = p.stderr.read().decode('utf-8')
		current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		with open('/root/hyh/cloud/logs/git.log', 'w') as f:
			f.write(current_time + '\n' + git_out + '\n' + str(status_code))

		with open('/root/hyh/cloud/logs/git_err.log', 'w') as f:
			f.write(current_time + '\n' + git_err + '\n' + str(status_code))
	else:
		p = subprocess.Popen('git clone '+sys.argv[1],bufsize=1,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		p.wait()
		status_code = p.returncode  #git clone状态码，0表示克隆成功
		git_out = p.stdout.read().decode('utf-8')
		git_err = p.stderr.read().decode('utf-8')
		current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		with open('/root/hyh/cloud/logs/git.log', 'w') as f:
			f.write(current_time + '\n' + git_out + '\n' + str(status_code))

		with open('/root/hyh/cloud/logs/git_err.log', 'w') as f:
			f.write(current_time + '\n' + git_err + '\n' + str(status_code))
	if not status_code:
		return True	
######################拉完代码#################



################mvn构建war包####################

def mvn():
	os.chdir(project_dir)
	m = subprocess.Popen('mvn clean compile package -P nexus,rd-test -Dmaven.test.skip=true',bufsize=1,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	m.wait()
	m_status_code = m.returncode
	mvn_log = m.stdout.read().decode('utf-8')
	mvn_err_log = m.stderr.read().decode('utf-8')
	current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	with open('/root/hyh/cloud/logs/mvn.log', 'w') as f:
		f.write(current_time + '\n' + mvn_log + '\n' + str(m_status_code))
	
	if not m_status_code:
		return True		
	#with open('root/hyh/cloud/logs/mvn_err.log', 'w') as f:
	#	f.write(current_time + '\n' + mvn_err_log + '\n' + str(m_status_code))
#####################mvn构建结束####################

servant_cfg_dir = '/data/docker_conf/' + app_name	#servant.property文件位置

#################修改保存配置文件##################
def save_cfg():
	is_exist_app = os.path.isdir(app_dir)   #判断app目录是否存在,存在返回true,否则返回false
	is_exist_cfg = os.path.isdir(servant_cfg_dir)
	if is_exist_app:
		shutil.rmtree(app_dir)
		shutil.move(src_dir,all_app_dir)
		if is_exist_cfg:
			servant = app_dir + '/WEB-INF/classes/conf/servant.properties'
			shutil.copy(servant,servant_cfg_dir)
			return True
		else:
			os.makedirs(servant_cfg_dir)
			servant = app_dir + '/WEB-INF/classes/conf/servant.properties'
			shutil.copy(servant,servant_cfg_dir)
			return True
		
	else:
		shutil.move(src_dir,all_app_dir)
		if is_exist_cfg:
			servant = app_dir + '/WEB-INF/classes/conf/servant.properties'
			shutil.copy(servant,servant_cfg_dir)
			return True
		else:
			os.makedirs(servant_cfg_dir)
			servant = app_dir + '/WEB-INF/classes/conf/servant.properties'
			shutil.copy(servant,servant_cfg_dir)
			return True

##################修改配置文件结束############


################制作镜像####################

def do_img():
	os.chdir(all_app_dir)
	is_exist_app = os.path.isdir(app_dir)
	if is_exist_app:
		dockerfile = 'FROM clean/tomcat_v3\n' + 'MAINTAINER test "docker@kkd.com"\n' + 'ADD ' + app_name + '  /usr/local/apache-tomcat-7.0.61/webapps/' + app_name + '\n' + 'ENV LANG en_US.UTF-8' + '\n' + 'EXPOSE 22 8080' + '\n' + 'ENTRYPOINT ["/usr/local/apache-tomcat-7.0.61/bin/catalina.sh", "run" ]'
		with open(all_app_dir+'/Dockerfile', 'w') as f:
			f.write(dockerfile)
		build_img_cmd = 'docker build -t=' + img_name +'  .'
		
		img_obj = subprocess.Popen(build_img_cmd,bufsize=1,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		img_obj.wait()
		img_obj_status_code = img_obj.returncode
		img_log = img_obj.stdout.read().decode('utf-8')
		#img_err_log = img_obj.stderr.read().decode('utf-8')
		current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		with open('/root/hyh/cloud/logs/img_build.log', 'w') as f:
			f.write(current_time + '\n' + img_log + '\n' + str(img_obj_status_code))
		if not img_obj_status_code:
			img_save_cmd = 'docker save ' + img_name + ' > ' + '/data/history_img/' + img_name + '.tar'
			img_save = subprocess.Popen(img_save_cmd,bufsize=1,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			img_save.wait()
			img_save_status_code = img_save.returncode
			img_save_log = img_save.stdout.read().decode('utf-8')
        #img_err_log = img_obj.stderr.read().decode('utf-8')
			current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
			with open('/root/hyh/cloud/logs/img_save.log', 'w') as f:
				f.write(current_time + '\n' + img_save_log + '\n' + str(img_save_status_code))
			

################制作镜像结束###############
if __name__ == '__main__':
	git_res = get_code()
	if git_res:
		mvn_res = mvn()
		if mvn_res:
			save_cfg_res = save_cfg()
		else:
			mvn_err = "mvn打包编译失败，请检查"
			with open("/root/hyh/cloud/logs/mvncompile_err.log",'w') as f:
				f.write(mvn_err)
			sys.exit(2)
	else:
		err = "git获取代码失败，请检查"
		with open("/root/hyh/cloud/logs/git_err.log", 'a+') as f:
			f.write(err)
		sys.exit(1)

	if save_cfg_res:
		do_img()
