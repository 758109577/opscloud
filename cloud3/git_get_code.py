#!/usr/bin/python
# --*-- coding:utf-8 --*--
import subprocess
import sys,os
import time
if __name__ == '__main__':
	code_dir = "/data/code/project_git"
	os.chdir(code_dir)
	p = subprocess.Popen('git clone '+sys.argv[1],shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	while p.poll() is None:
		line = p.stdout.readline()
		line = line.strip()
		if line:
			print(line.decode('utf-8'))
	if p.returncode == 0:
		print("git success")
	else:
		print("git error")
