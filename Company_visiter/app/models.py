from django.db import models

# Create your models here.
class Registration_info(models.Model):

    id = models.AutoField(primary_key=True)
    uname=models.CharField(max_length=50)
    uemail=models.CharField(max_length=50)
    upass=models.CharField(max_length=10)
    
    def __str__(self):
        return self.uemail
    
class Add_new_visiter(models.Model):
    
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    phonenum = models.CharField(max_length=15)
    address = models.TextField()
    whomtomeet = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    reasontomeet = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    remark = models.CharField(max_length=20,default='')

    def __str__(self):
        return self.fullname

    