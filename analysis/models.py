from django.db import models

# Create your models here.
class usersignup(models.Model):
    username = models.CharField(max_length = 100)
    pswd = models.CharField(max_length = 100)
class Meta :
    db_table = "users"