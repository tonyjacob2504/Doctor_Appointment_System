from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class doctor(models.Model):
    name=models.CharField( max_length=50)
    email=models.EmailField( max_length=54)
    phone=models.CharField( max_length=50)
    specialization = models.CharField(max_length=100)
    qualification=models.CharField( max_length=50)
    experience=models.IntegerField()
    photo = models.ImageField(upload_to='doctor/')
    status = models.CharField(max_length=20, default='Pending')
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class user(models.Model):
    name=models.CharField( max_length=50)
    email=models.EmailField( max_length=54)
    phone=models.CharField( max_length=50)
    dob=models.DateField()
    gender=models.CharField(max_length=30)
    status = models.CharField(max_length=30, default="Pending")
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class complaint(models.Model):
    userprofile=models.ForeignKey(user,on_delete=models.CASCADE)
    date=models.CharField(max_length=100,default="")
    complaint=models.TextField()
    reply=models.TextField(null=True,blank=True)
    status=models.CharField(max_length=30,default="pending")

class dr_schedule(models.Model):
    doctors=models.ForeignKey(doctor,on_delete=models.CASCADE)
    date=models.DateField()
    day=models.CharField(max_length=20)
    from_time=models.TimeField()
    to_time=models.TimeField()

class dr_fee(models.Model):
    doctors=models.ForeignKey(doctor,on_delete=models.CASCADE)
    fees=models.IntegerField()

class appoinment(models.Model):
    schedule=models.ForeignKey(dr_schedule,on_delete=models.CASCADE)
    users=models.ForeignKey(user,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()
    status=models.CharField(max_length=20,default='pending')

class rating(models.Model):
    users=models.ForeignKey(user,on_delete=models.CASCADE)
    doctors=models.ForeignKey(doctor,on_delete=models.CASCADE)
    comment=models.CharField(max_length=30)
    ratings=models.IntegerField()
    date = models.DateField(auto_now_add=True)

class feedback(models.Model):
    userprofile = models.ForeignKey(user, on_delete=models.CASCADE)
    feedback = models.TextField()
    date = models.CharField(max_length=100, default="")