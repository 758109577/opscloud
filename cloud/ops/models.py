from django.db import models

# Create your models here.
class employee(models.Model):
	username = models.CharField(max_length=30)
	passwd = models.CharField(max_length=30)
	deptment = models.CharField(max_length=30)
	permission = models.IntegerField(null=True)

	def __str__(self):
		return self.username

class compiler(models.Model):
	compile_name = models.CharField(max_length=30)
	compile_ip = models.CharField(max_length=20)
	create_user_id = models.ForeignKey(employee)
	repertory_dir = models.CharField(max_length=30)
	
	def __str__(self):
		return self.compile_ip

class node_host(models.Model):
	node_name = models.CharField(max_length=30)
	node_ip = models.CharField(max_length=20)
	create_user_id = models.ForeignKey(employee)
	code_dir = models.CharField(max_length=30)

	def __str__(self):
		return self.node_ip

class server_info(models.Model):
	application = models.CharField(max_length=30)
	server_ip = models.CharField(max_length=20)
	server_port = models.IntegerField(null=True)
	image_id = models.CharField(max_length=50)
	container_id = models.CharField(max_length=50)
	container_status = models.CharField(max_length=10)

	def __str__(self):
		return self.server_ip
