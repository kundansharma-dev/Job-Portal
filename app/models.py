from django.db import models

# Create your models here.

# Master table Model
class UserMaster(models.Model):
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    otp=models.IntegerField()
    role=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    is_verified=models.BooleanField(default=False)
    is_created=models.DateTimeField(auto_now_add=True)
    is_updated=models.DateTimeField(auto_now_add=True)

# Candidate Model

class Candidate(models.Model):
    user_id=models.ForeignKey(UserMaster,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    address=models.CharField(max_length=150)
    dob=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    profile_pic=models.ImageField(upload_to="app/img/candidate")
    min_salary = models.CharField(max_length=100, default="0")
    max_salary = models.CharField(max_length=100, default="0")
    country=models.CharField(max_length=50)
    website=models.URLField(max_length=150)
    job_type=models.CharField(max_length=50)
    job_catagry=models.CharField(max_length=50)
    job_description=models.TextField()


# Company Table modle

class Company(models.Model):
    user_id=models.ForeignKey(UserMaster,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    company_name=models.CharField(max_length=150)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    contact=models.CharField(max_length=50)
    address=models.CharField(max_length=150)
    logo_pic=models.ImageField(upload_to="app/img/company")


