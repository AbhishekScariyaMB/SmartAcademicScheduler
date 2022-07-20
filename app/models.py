from django.db import models

#--------------------SCHEDULER----------------------------

import random as rnd
import datetime
from django.db import models
import math
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from datetime import timedelta, date


time_slots = (
    ('9:30 - 10:30', '9:30 - 10:30'),
    ('10:30 - 11:30', '10:30 - 11:30'),
    ('11:30 - 12:30', '11:30 - 12:30'),
    ('12:30 - 1:30', '12:30 - 1:30'),
    ('2:30 - 3:30', '2:30 - 3:30'),
    ('3:30 - 4:30', '3:30 - 4:30'),
    ('4:30 - 5:30', '4:30 - 5:30'),
)
DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)

POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1

#--------------------SCHEDULER----------------------------

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
    descrip=models.CharField(max_length=300)
    status=models.CharField(max_length=5,default=1)

    class Meta:
        db_table = "department"

       

class teacher(models.Model):
    name=models.CharField(max_length=50)
    dob=models.DateField(null=True)
    gender=models.CharField(max_length=15)
    address=models.CharField(max_length=200)
    email=models.CharField(max_length=30)
    phone=models.CharField(max_length=20)
    dept_id=models.BigIntegerField(default=0)
    photo=models.CharField(max_length=100)
    qualification=models.CharField(max_length=30)
    login_id=models.BigIntegerField()

    #Timetable generator 
    uid = models.CharField(max_length=10,default="None")

    def __str__(self):
        return f'{self.uid} {self.name}'
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

class student(models.Model):
    app_id=models.BigIntegerField(default=0)
    batch_id=models.CharField(max_length=100,default=0)
    login_id=models.BigIntegerField(default=0)
    class Meta:
        db_table = "student"   



class Room(models.Model):
    r_number = models.CharField(max_length=10)
    seating_capacity = models.IntegerField(default=0)

    #additional fields for project
    status=models.CharField(max_length=5,default=1)     
    def __str__(self):
        return self.r_number
    class Meta:
        db_table = "room"  

class MeetingTime(models.Model):
    pid = models.BigIntegerField(primary_key=True)
    time = models.CharField(max_length=50, choices=time_slots, default='11:30 - 12:30')
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)

    def __str__(self):
        return f'{self.pid} {self.day} {self.time}'
    class Meta:
        db_table = "meetingtime"        

class subject(models.Model):
    subject_number = models.CharField(max_length=10, primary_key=True) #subject code
    subject_name = models.CharField(max_length=40)
    max_numb_students = models.CharField(max_length=65)
    teachers = models.ManyToManyField(teacher)
    dept_id=models.BigIntegerField(default=0)
    #additional fields for project
    subject_type=models.CharField(max_length=10,default="theory")
    

    def __str__(self):
        return f'{self.subject_number} {self.subject_name}'
    class Meta:
        db_table = "subject"        

class course(models.Model):
    #------------------------------------------
    course_name=models.CharField(max_length=50)
    subjects = models.ManyToManyField(subject)
    #------------------------------------------
    duration=models.CharField(max_length=5)
    dept_id=models.BigIntegerField()
    status=models.CharField(max_length=5,default=1)
    fee=models.CharField(max_length=7,default=25000)
    class Meta:
        db_table = "course"    
    @property
    def get_subjects(self):
        return self.subjects

    def __str__(self):
        return self.course_name
    class Meta:
        db_table = "course"  

class batch(models.Model):
    batch_id = models.CharField(max_length=25, primary_key=True)
    course = models.ForeignKey(course, on_delete=models.CASCADE,default=1)
    num_class_in_week = models.IntegerField(default=0)
    subject = models.ForeignKey(subject, on_delete=models.CASCADE, blank=True, null=True)
    meeting_time = models.ForeignKey(MeetingTime, on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey(Room,on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(teacher, on_delete=models.CASCADE, blank=True, null=True)

    class_teacher=models.BigIntegerField(default=0)
    semester=models.BigIntegerField(default=0)
    status= models.CharField(max_length=25,default="batched")

    def set_room(self, room):
        batch = batch.objects.get(pk = self.batch_id)
        batch.room = room
        batch.save()

    def set_meetingTime(self, meetingTime):
        batch = batch.objects.get(pk = self.batch_id)
        batch.meeting_time = meetingTime
        batch.save()

    def set_teacher(self, teacher):
        batch = batch.objects.get(pk=self.batch_id)
        batch.teacher = teacher
        batch.save()
    class Meta:
        db_table = "batch"  


class attendence(models.Model):
    student_id=models.CharField(max_length=10)
    date=models.DateField()
    day=models.CharField(max_length=50)
    att_str=models.CharField(max_length=200)
    class Meta:
        db_table = "attendence" 

class attstring(models.Model):
    batch_id = models.CharField(max_length=25)
    day=models.CharField(max_length=50)
    def_string=models.CharField(max_length=200)
    class Meta:
        db_table = "attstring" 

class studymaterial(models.Model):
    subject_number = models.CharField(max_length=10)            
    material=models.CharField(max_length=100)
    title=models.CharField(max_length=30)
    teacher_id = models.BigIntegerField(default=0)

    class Meta:
        db_table = "studymaterial"

class assignment(models.Model):
    subject_number = models.CharField(max_length=10)
    title = models.CharField(max_length=30)
    problem = models.CharField(max_length=100)
    teacher_id = models.BigIntegerField(default=0)
    fromtime = models.DateTimeField()
    totime = models.DateTimeField()
    status = models.CharField(max_length=10,default=1)
    class Meta:
        db_table = "assignment"

class submission(models.Model):
    assignment_id = models.BigIntegerField(default=0)
    answer = models.CharField(max_length=100)
    marks = models.CharField(max_length=3)    
    student_id = models.BigIntegerField()
    class Meta:
        db_table = "submission"    