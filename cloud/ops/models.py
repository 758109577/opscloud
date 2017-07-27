from django.db import models

# Create your models here.
class employee(models.Model):
	username = models.CharField(max_length=30)
	passwd = models.CharField(max_length=30)
	deptment = models.CharField(max_length=30)

	def __str__(self):
		return self.username
