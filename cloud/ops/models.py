from django.db import models

# Create your models here.
class employee(models.Model):
	username = models.CharField(max_length=30)
	passwd = models.CharField(max_length=30)
	deptment = models.CharField(max_length=30)

	def __str__(self):
		return self.username

class compiler(models.Model):
	compile_name = models.CharField(max_length=30)
	compile_ip = models.CharField(max_length=20)
	create_user_id = models.ForeignKey(employee)
	repertory_dir = models.CharField(max_length=30)
	
	def __str__(self):
		return self.compile_ip
