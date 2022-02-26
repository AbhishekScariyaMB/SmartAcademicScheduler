from django.db import models

# Create your models here.

class login(models.Model):
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=20)
    utype_id=models.BigIntegerField()
    status=models.CharField(max_length=5,default=1)

    class Meta:
        db_table = "login"

class utype(models.Model):
    name=models.CharField(max_length=15)

    class Meta:
        db_table = "utype"

class department(models.Model):
    name=models.CharField(max_length=50)
    status=models.CharField(max_length=5,default=1)

    class Meta:
        db_table = "department"

class course(models.Model):
    name=models.CharField(max_length=50)
    duration=models.CharField(max_length=5)
    dept_id=models.BigIntegerField()
    status=models.CharField(max_length=5,default=1)
    class Meta:
        db_table = "course"        

class teacher(models.Model):
    name=models.CharField(max_length=50)
    dob=models.DateField()
    gender=models.CharField(max_length=15)
    address=models.CharField(max_length=200)
    email=models.CharField(max_length=30)
    phone=models.CharField(max_length=20)
    dept_id=models.BigIntegerField(default=0)
    photo=models.CharField(max_length=100)
    qualification=models.CharField(max_length=30)
    login_id=models.BigIntegerField()
    class Meta:
        db_table = "teacher"

class application(models.Model):
    name=models.CharField(max_length=50)
    dob=models.DateField()
    gender=models.CharField(max_length=15)
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)
    email=models.CharField(max_length=30)
    photo=models.CharField(max_length=100)
    course_id=models.BigIntegerField(default=0)
    stage=models.CharField(max_length=15,default='1')
    score=models.DecimalField(max_digits=4, decimal_places=2,default=0)
    class Meta:
        db_table = "application"        

class parent(models.Model):
    fname=models.CharField(max_length=50)
    mname=models.CharField(max_length=50)
    fmail=models.CharField(max_length=30)
    mmail=models.CharField(max_length=30)
    fjob=models.CharField(max_length=30)
    mjob=models.CharField(max_length=30)
    fphone=models.CharField(max_length=20)
    mphone=models.CharField(max_length=20)
    app_id=models.BigIntegerField(default=0)
    class Meta:
        db_table = "parent"

class record(models.Model):
    tenth=models.DecimalField(max_digits=4, decimal_places=2)
    twelfth=models.DecimalField(max_digits=4, decimal_places=2)
    ug=models.DecimalField(max_digits=4, decimal_places=2,null=True)
    certificatetenth=models.CharField(max_length=100)
    certificatetwelfth=models.CharField(max_length=100)
    certificateug=models.CharField(max_length=100)
    app_id=models.BigIntegerField(default=0)
    class Meta:
        db_table = "record"   

