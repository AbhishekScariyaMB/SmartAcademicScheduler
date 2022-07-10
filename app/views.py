from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from app.models import login , utype, department, course, teacher, application, parent, record, student, batch, subject, Room, time_slots, DAYS_OF_WEEK, MeetingTime
from django.contrib import messages
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import cms.settings
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from matplotlib import pyplot as plt
#------------------------------
import random as rnd
POPULATION_SIZE = 6
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05
D = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
HOURS=[1,2,3,4,5,6]
#------------------------------
class Data:
    def __init__(self):
        self._rooms = Room.objects.all()
        self._meetingTimes = MeetingTime.objects.all()
        self._teachers = teacher.objects.all()
        self._subjects = subject.objects.all()
        self._courses = course.objects.all()

    def get_rooms(self): return self._rooms

    def get_teachers(self): return self._teachers

    def get_subjects(self): return self._subjects

    def get_courses(self): return self._courses

    def get_meetingTimes(self): return self._meetingTimes


class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self): return self._numberOfConflicts

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        occupied_slots = {}
        batchs = batch.objects.all()
        for batche in batchs:
            course = batche.course
            n = batche.num_class_in_week         
            if n <= len(MeetingTime.objects.all()):
                subjects = course.subjects.all()
                for subject in subjects:
                    for i in range(n // len(subjects)):
                        crs_inst = subject.teachers.all()
                        newClass = Class(self._classNumb, course, batche.batch_id, subject)
                        self._classNumb += 1
                        a = data.get_meetingTimes()[rnd.randrange(0, len(MeetingTime.objects.all()))]
                        newClass.set_meetingTime(a)                         
                        newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                        newClass.set_teacher(crs_inst[rnd.randrange(0, len(crs_inst))])
                        self._classes.append(newClass)
            else:
                n = len(MeetingTime.objects.all())
                subjects = course.subjects.all()
                for subject in subjects:
                    for i in range(n // len(subjects)):
                        crs_inst = subject.teachers.all()
                        newClass = Class(self._classNumb, course, batche.batch_id, subject)
                        self._classNumb += 1
                        newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, len(MeetingTime.objects.all()))])

                

                        newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                        newClass.set_teacher(crs_inst[rnd.randrange(0, len(crs_inst))])
                        self._classes.append(newClass)

              

        return self

    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        #OBTAIN teacher DICT FOR HOUR CALCULATION
        dat=Data()
        teachers = dat.get_teachers()
        x = (teachers[l].uid for l in range(len(teachers)))
        y = 0
        hour_count = dict.fromkeys(x, y)
       

        for i in range(len(classes)):
            if classes[i].room.seating_capacity < int(classes[i].subject.max_numb_students):
                self._numberOfConflicts += 1
            
            for x,y in hour_count.items():
                if classes[i].teacher.uid == x:
                    hour_count[x]+=1    

            for j in range(len(classes)):
                if j >= i:
                    if (classes[i].meeting_time == classes[j].meeting_time) and \
                            (classes[i].batch_id != classes[j].batch_id) and (classes[i].batch == classes[j].batch):
                        if classes[i].room == classes[j].room:
                            self._numberOfConflicts += 1
                        if classes[i].teacher == classes[j].teacher:
                            self._numberOfConflicts += 1
        return 1 / (1.0 * self._numberOfConflicts + 1)


class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = [Schedule().initialize() for i in range(size)]

    def get_schedules(self):
        return self._schedules


class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Class:
    def __init__(self, id, course, batch, subject):
        self.batch_id = id
        self.course = course
        self.subject = subject
        self.teacher = None
        self.meeting_time = None
        self.room = None
        self.batch = batch

    def get_id(self): return self.batch_id

    def get_course(self): return self.course

    def get_subject(self): return self.subject

    def get_teacher(self): return self.teacher

    def get_meetingTime(self): return self.meeting_time

    def get_room(self): return self.room

    def set_teacher(self, teacher): self.teacher = teacher

    def set_meetingTime(self, meetingTime): self.meeting_time = meetingTime

    def set_room(self, room): self.room = room


data = Data()


def context_manager(schedule):
    classes = schedule.get_classes()
    context = []
    cls = {}
    for i in range(len(classes)):
        cls["batch"] = classes[i].batch_id
        cls['course'] = classes[i].course.course_name
        cls['subject'] = f'{classes[i].subject.subject_name} ({classes[i].subject.subject_number}, ' \
                        f'{classes[i].subject.max_numb_students}'
        cls['room'] = f'{classes[i].room.r_number} ({classes[i].room.seating_capacity})'
        cls['teacher'] = f'{classes[i].teacher.name} ({classes[i].teacher.uid})'
        cls['meeting_time'] = [classes[i].meeting_time.pid, classes[i].meeting_time.day, classes[i].meeting_time.time]
        context.append(cls)
    return context


def home(request):
    return render(request, 'index.html', {})


def timetable(request):
    schedule = []
    population = Population(POPULATION_SIZE)
    generation_num = 0
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    geneticAlgorithm = GeneticAlgorithm()
    while population.get_schedules()[0].get_fitness() != 1.0:
        generation_num += 1
        print('\n> Generation #' + str(generation_num))
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        schedule = population.get_schedules()[0].get_classes()

    wb = Workbook()
    batches=batch.objects.all()
    hoursss=MeetingTime.objects.all()
    for b in batches:
        ws = wb.create_sheet(b.batch_id)
        ws['A1']="DAY"
        i=0
        for row in ws.iter_rows(min_row=2, max_col=1, max_row=6):
            for cell in row:
                cell.value=str(D[i])
                i+=1
        i=0
        for col in ws.iter_cols(min_col=2, max_col=7, max_row=1):
            for cell in col:
                cell.value=HOURS[i]
                i+=1        
    for classs in schedule:
        mysheet=wb[classs.batch]
        if(classs.meeting_time.pid) in range(1,7):
            mysheet.cell(row=2,column=classs.meeting_time.pid+1).value=str(classs.subject.subject_number)+","+str(classs.teacher.uid)+","+str(classs.room.r_number)
        elif(classs.meeting_time.pid) in range(7,13): 
            if(classs.meeting_time.pid%6==0):
                mysheet.cell(row=3,column=7).value=str(classs.subject.subject_number)+","+str(classs.teacher.uid)+","+str(classs.room.r_number)    
            else:
                mysheet.cell(row=3,column=(classs.meeting_time.pid%6)+1).value=str(classs.subject.subject_number)+","+str(classs.teacher.uid)+","+str(classs.room.r_number)
        elif(classs.meeting_time.pid) in range(13,19):    
             if(classs.meeting_time.pid%6==0):
                 mysheet.cell(row=4,column=7).value=str(classs.subject.subject_number)+","+str(classs.teacher.uid)+","+str(classs.room.r_number)
             else:
                 mysheet.cell(row=4,column=(classs.meeting_time.pid%6)+1).value=str(classs.subject.subject_number)+","+str(classs.teacher.uid)+","+str(classs.room.r_number)
        elif(classs.meeting_time.pid) in range(19,25):    
            if(classs.meeting_time.pid%6==0):
                 mysheet.cell(row=5,column=7).value=str(classs.subject.subject_number)+","+str(classs.teacher.uid)+","+str(classs.room.r_number)
            else:
                 mysheet.cell(row=5,column=(classs.meeting_time.pid%6)+1).value=str(classs.subject.subject_number)+","+str(classs.teacher.uid)+","+str(classs.room.r_number)
        elif(classs.meeting_time.pid) in range(25,31):    
            if(classs.meeting_time.pid%6==0):
                 mysheet.cell(row=6,column=7).value=str(classs.subject.subject_number)+","+str(classs.teacher.uid)+","+str(classs.room.r_number)
            else:
                 mysheet.cell(row=6,column=(classs.meeting_time.pid%6)+1).value=str(classs.subject.subject_number)+","+str(classs.teacher.uid)+","+str(classs.room.r_number)   
    f=wb["Sheet"]
    wb.remove(f)
    wb.save('D:\Main Project\cms\\timetable\\timetable.xlsx')        

    return render(request, 'timetable.html', {'schedule': schedule, 'batchs': batch.objects.all(),
                                              'times': MeetingTime.objects.all()})


#----------------------------------------------------------------------------------------------------------------------------------







@cache_control(no_cache=True, must_revalidate=True)
def func():
  #some code
  return

# Create your views here.
def home(request):
    return render(request,'home.html')

def depts(request):
    data=department.objects.all()
    dep={
        "dept_no":data
    }
    return render(request,'departments.html',dep) 

def courses(request):
    data=department.objects.all()
    data2=course.objects.all()
    d={
        "dept_data":data,
        "course_data":data2,
    }
    return render(request,'courses.html',d) 

def log_in(request):
    return render(request,'login.html')    

def user_login(request):
    dat=login.objects.all()
    dat2=utype.objects.all()
    flag=0
    un=request.POST.get("username")
    pw=request.POST.get("password")
    for d in dat:
        if d.username==un and d.password==pw  and d.status=='1':
            request.session['id']=d.id
            flag =1
            id = request.session['id']
            data=login.objects.get(id=id)
            for e in dat2:
                if d.utype_id==e.id:
                    request.session['utype']=d.utype_id
                    if e.name=='admin':
                        return redirect('/dash/')
                    elif e.name=='teacher':
                        dat3=teacher.objects.get(login_id=d.id)
                        if dat3.name=='no data':
                            return render(request, 'teacherregister.html')
                        else:    
                            return redirect('/dash2/')  
                    elif e.name=='hod':
                        return redirect('/dash3/')     
                    elif e.name=='admission':
                       return redirect('/dash4/')
                    else:
                        return render(request, 'login.html')         
    if flag==0:
        messages.error(request,'Username or Password is incorrect!')
        return redirect('/login/')         

def test_form(request):
    return render(request, 'form-samples-copy.html')
def dash(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    # id = request.session['id']
    # data=login.objects.get(id=id)


    # data=application.objects.all()
    # admitted=0
    # rejected=0
    # ongoing=0
    # for i in data:
    #     if i.stage=='3':
    #         admitted+=1
    #     elif i.stage=='0':
    #         rejected+=1
    #     else:
    #         ongoing+=1    


    # y = np.array([ongoing, admitted, rejected])
    # mylabels = ["Ongoing", "Admitted", "Rejected"]
    # plt.legend()
    # plt.pie(y, labels = mylabels)


    # total=[ongoing,admitted,rejected]
    # title = plt.title('Admissions')
    # title.set_ha("left")
    # plt.gca().axis("equal")
    # pie = plt.pie(total, startangle=0)
    # labels=["Ongoing", "Admitted", "Rejected"]
    # plt.legend(pie[0],labels, bbox_to_anchor=(0.8,0.5), loc="center right", fontsize=10,bbox_transform=plt.gcf().transFigure)
    # plt.subplots_adjust(left=0.0, bottom=0.1, right=0.45)    
    # plt.savefig('D:\Main Project\cms\static\\assets\images\pieadmission.png')


    return render(request, 'dashboard.html')  

def dash2(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login') 
    return render(request, 'teacher.html')   

def dash3(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login') 
    return render(request, 'hod.html')   

def dash4(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login') 
    return render(request, 'incharge.html')           

def dashboardref(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    uid=request.session.get('utype') 
    print(uid)
    if (uid == 1):   
        data=application.objects.all()
        return render(request, 'dashboard.html') 
    elif (uid == 2):
        return render(request, 'teacher.html')    
    elif (uid == 3):
        return render(request, 'hod.html')   
    else:
        return render(request, 'incharge.html')      

def deptadd(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    return render(request, 'deptadd.html')    

def deptaddval(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    name = request.POST['name'] 
    descrip = request.POST['descrip']
    data=department.objects.all()
    for i in data:
        if i.name == name:
            messages.warning(request, 'Department already exists... Insertion failed!')
            return redirect('/deptadd/')
    dept=department.objects.create(name=name,descrip=descrip)
    dept.save()
    messages.success(request, 'Department added successfully...!')
    return redirect('/deptadd/')

def deptview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    data=department.objects.all()
    dept={
        "dept_no":data
    }
    return render(request,"deptview.html",dept)

def depteditview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    data=department.objects.all()
    dept={
        "dept_no":data
    }
    return render(request,"depteditview.html",dept)    

def deptedit(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    data=department.objects.all()
    id=request.POST.get("id")
    for d in data:
        if int(id)==d.id:
          dept={"d":d}
          return render(request,"deptedit.html",dept)

def deptupdate(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.POST.get("id")
    data=department.objects.get(pk=id)
    data2=course.objects.filter(dept_id=id)
    data.name=request.POST.get("name")
    data.status=request.POST.get("status")
    data.descrip=request.POST.get("descrip")
    if data.status=='0':    
        for c in data2:
            c.status=data.status
            c.save()
    data.save()
    
    messages.success(request, 'Department updated successfully...!')
    return redirect("/depteditview/")

def logout(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/login')
    request.session.flush()
    return HttpResponseRedirect('/login')

def courseadd(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    data=department.objects.all()
    dept={
        "dept_no":data
    }
    return render(request,"courseadd.html",dept)  

def courseaddval(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    name = request.POST['name'] 
    duration = request.POST['duration']
    dept_id = request.POST['dept_id']  
    fee = request.POST['fee']
    data2 = course.objects.all()
    for i in data2:
        if i.course_name == name:
            messages.warning(request, 'Course already exists..! Insertion failed!')
            return redirect('/courseadd/')

    c=course.objects.create(course_name=name,duration=duration,dept_id=dept_id,fee=fee)
    c.save()
    messages.success(request, 'Course added successfully...!')
    return redirect('/courseadd/')    
    
def courseview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    data1=course.objects.all()
    data2=department.objects.all()
    data={
        "course":data1,
        "dept":data2
    }
    

    return render(request,"courseview.html",data)    

def courseeditview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    data1=course.objects.all()
    data2=department.objects.all()
    data={
        "course":data1,
        "dept":data2
    }
    

    return render(request,"courseeditview.html",data)       

def courseedit(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    data=course.objects.all()
    data2=department.objects.all()
    cid=request.POST.get("cid")
    for c in data:
        if int(cid)==c.id:
          dat={"c":c,"d":data2}
          return render(request,"courseedit.html",dat)

def courseupdate(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.POST.get("id")
    data=course.objects.get(pk=id)
    data.name=request.POST.get("name")
    data.duration=request.POST.get("duration")
    data.fee = request.POST['fee']
    data.dept_id=request.POST.get("dept")
    data.status=request.POST.get("status")
    data.save()
    messages.success(request, 'Course updated successfully...!')
    return redirect("/courseeditview/")

def useradd(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    return render(request, 'useradd.html')    

def teacheradd(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    data=department.objects.all()
    password = User.objects.make_random_password(length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889") 
    dept={
        "dept_no":data,
        "password":password
    }
    return render(request, 'teacheradd.html',dept)

def admissionadd(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    password = User.objects.make_random_password(length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889") 
    dat={
        "password":password
    }
    return render(request, 'admissionadd.html',dat)

def admissiongen(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    email = request.POST['email'] 
    password = request.POST['password']
    mailto = request.POST['mailto']
    data=login.objects.all()
    for d in data:
        if d.username == email:
            messages.warning(request, 'User already exists...!')
            return redirect('/useradd/')
    l=login.objects.create(username=email,password=password,utype_id=4,status='1')
    subject = 'Login credentials'
    message = f'Welcome to Smart Academic Scheduler. Here are your login credentials to manage student admission.\nUsername: {email}\nPassword: {password}'
    email_from = cms.settings.EMAIL_HOST_USER
    recipient_list = [mailto]
    send_mail( subject, message, email_from, recipient_list )
    l.save()
    login_id=l.id
    messages.success(request, 'Admission in-charge added successfully...!')
    return redirect('/useradd/')    

def teachergen(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    email = request.POST['email'] 
    password = request.POST['password']
    dept_id = request.POST['dept_id']  
    uid = request.POST['uid']
    data=login.objects.all()
    for d in data:
        if d.username == email:
            messages.warning(request, 'User already exists...!')
            return redirect('/useradd/')
    l=login.objects.create(username=email,password=password,utype_id=2,status='1')
    l.save()
    login_id=l.id
    t=teacher.objects.create(name='no data',phone='no data',dob=None,gender='no data',address='no data',email=email,dept_id=dept_id,qualification='no data',login_id=login_id,uid=uid)
    t.save()
    subject = 'Login credentials'
    message = f'Welcome to Smart Academic Scheduler. Here are your login credentials.\nUsername: {email}\nPassword: {password}'
    email_from = cms.settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )
    messages.success(request, 'Teacher added successfully...!')
    return redirect('/useradd/')    

def userview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    data1=login.objects.filter(~Q(utype_id='1'))
    data2=utype.objects.all()
    data={
        "login":data1,
        "utype":data2
    }
    return render(request, 'userview.html',data)

def usereditview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    data1=login.objects.filter(~Q(utype_id='1'))
    data2=utype.objects.all()
    data={
        "login":data1,
        "utype":data2
    }
    return render(request, 'usereditview.html',data)        

def useredit(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.POST.get('id')
    data1=login.objects.get(pk=id)    
    data2=utype.objects.all()
    data={
          'user':data1,
          'utype':data2,  
            }
    return render(request, 'useredit.html',data)

def userupdate(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.POST.get('id')
    data1=login.objects.get(pk=id)    
    data1.username=request.POST.get('username')
    data1.password=request.POST.get('password')
    data1.utype_id=request.POST.get('utype')   
    data1.status=request.POST.get('status')
    data1.save()
    return redirect('/usereditview/')

def teacherregister(request):
    uid=request.session['id']
    data=teacher.objects.get(login_id=uid)
    data.name=request.POST.get("name")
    data.address=request.POST.get("address")
    data.gender=request.POST.get("gender")
    data.dob=request.POST.get("dob")
    data.qualification=request.POST.get("qualification")
    data.phone=request.POST.get("phone")

    Photo=request.FILES['photo']
    fs=FileSystemStorage()
    fn=fs.save(Photo.name, Photo)
    uploaded_file_url=fs.url(fn)
    data.photo=uploaded_file_url

    data.save()
    return redirect('/login/')

def sethod(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    data2=department.objects.all()
    dat={
        
        "department":data2,
    }
    return render(request, 'sethod.html', dat)    

def deptteacherview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.POST.get("id") 
    data=teacher.objects.filter(dept_id=id) 
    dat={
        "teacher":data,     
    } 
    return render(request,'deptteacherview.html',dat)

def hodupdate(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.POST.get("id")
    hod=teacher.objects.get(pk=id)
    teachers=teacher.objects.filter(dept_id=hod.dept_id)
    loginfo=login.objects.filter(utype_id='3')
    for t in teachers:
        for l in loginfo:
            if t.login_id == l.id:
                l.utype_id='2'
                l.save()
    hodlogin=login.objects.get(pk=hod.login_id) 
    hodlogin.utype_id='3'
    hodlogin.save()           
    return redirect('/sethod/')

def hodview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    l=login.objects.filter(utype_id='3')
    t=teacher.objects.all()
    d=department.objects.all()
    data={
        "loginfo":l,
        "teachers":t,
        "dept":d,
    }
    return render(request,'hodview.html',data)    

def appli(request):
    c=course.objects.filter(status='1')
    data={
        "course":c,
    }
    return render(request,'application.html',data)   

def apply(request):
    name=request.POST.get('name') 
    dob=request.POST.get('dob') 
    gender=request.POST.get('gender') 
    address=request.POST.get('address')
    phone=request.POST.get('phone')
    email=request.POST.get('email')
    course=request.POST.get('course')
    fname=request.POST.get('fname')
    mname=request.POST.get('mname')
    fmail=request.POST.get('fmail')
    mmail=request.POST.get('mmail')
    fjob=request.POST.get('fjob')
    mjob=request.POST.get('mjob')
    fphone=request.POST.get('fphone')
    mphone=request.POST.get('mphone')
    tenth=request.POST.get('tenth')
    twelfth=request.POST.get('twelfth')
    ug=request.POST.get('ug')
    
    data=application.objects.create(name=name,dob=dob,gender=gender,address=address,phone=phone,email=email,course_id=course)

    #Photo upload
    Photo=request.FILES['photo']
    fs=FileSystemStorage()
    fn=fs.save(Photo.name, Photo)
    uploaded_file_url=fs.url(fn)
    data.photo=uploaded_file_url
    data.save()


    #Certificate upload
    certificatetenth=request.FILES['certificatetenth']
    fs=FileSystemStorage()
    fn=fs.save(certificatetenth.name, certificatetenth)
    uploaded_file_url=fs.url(fn)
    certificatetenth=uploaded_file_url

    certificatetwelfth=request.FILES['certificatetwelfth']
    fs=FileSystemStorage()
    fn=fs.save(certificatetwelfth.name, certificatetwelfth)
    uploaded_file_url=fs.url(fn)
    certificatetwelfth=uploaded_file_url  

    certificateug=request.FILES['certificateug']
    fs=FileSystemStorage()
    fn=fs.save(certificateug.name, certificateug)
    uploaded_file_url=fs.url(fn)
    certificateug=uploaded_file_url  
    data3=record.objects.create(tenth=tenth,twelfth=twelfth,ug=ug,certificatetenth=certificatetenth,certificatetwelfth=certificatetwelfth,certificateug=certificateug,app_id=data.id)

    data3.save()

    data2=parent.objects.create(fname=fname,mname=mname,fmail=fmail,mmail=mmail,fjob=fjob,mjob=mjob,fphone=fphone,mphone=mphone,app_id=data.id)
    data2.save()
    
    return render(request,'home.html')

def courseapp(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    c=course.objects.all()
    d=department.objects.all()
    data={
        "course":c,
        "dept":d,
    }
    return render(request,'courseapp.html',data)

def appliview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    cid=request.POST.get("cid")
    cname=request.POST.get("cname")
    a=application.objects.filter(course_id=cid,stage__lt=2)
    r=record.objects.all()
    data={
        "app":a,
        "rec":r,
        "course":cname,
    }
    return render(request,'appliview.html',data)

def confirmapp(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.POST.get("aid")  
    a=application.objects.get(id=id)
    c=course.objects.get(id=a.course_id)
    subject = 'Application confirmation'
    message = f'Welcome to EduExpert.\nApplicant name: {a.name}\nPhone: {a.phone}\nCourse: {c.course_name}\n\n\n Please contact us to confirm your application. You can do so by replying to this email or contacting us at +919228833746.'
    email_from = cms.settings.EMAIL_HOST_USER
    recipient_list = [a.email]
    send_mail( subject, message, email_from, recipient_list )
    a.stage='1.25'
    a.save()
    snd1=application.objects.filter(course_id=c.id,stage__lt=2)
    snd2=record.objects.all()
    data={
        "app":snd1,
        "rec":snd2,
        "course":c.course_name,
    }
    return render(request,'appliview.html',data)

def confirmedapp(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.POST.get("aid")  
    a=application.objects.get(id=id)
    c=course.objects.get(id=a.course_id)
    a.stage='1.5'
    a.save()
    snd1=application.objects.filter(course_id=c.id,stage__lt=2)
    snd2=record.objects.all()
    data={
        "app":snd1,
        "rec":snd2,
        "course":c.course_name,
    }
    return render(request,'appliview.html',data)

def ranklistview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    c=course.objects.all()
    d=department.objects.all()
    data={
        "course":c,
        "dept":d,
    }
    return render(request,'ranklistview.html',data)    

def ranklist(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    cid=request.POST.get("cid")
    a=application.objects.filter(stage = '1.5',course_id=cid) 
    c=course.objects.get(id=cid) 
    r=record.objects.all()
    for i in a:
        for j in r:
            if i.id == j.app_id:
                if j.ug is not None:
                    i.score=(j.tenth + j.twelfth + j.ug)/3
                    i.save()
                else:    
                    i.score=((0.3*j.tenth+0.7*j.twelfth)/3)
                    i.save()
    b=application.objects.filter(stage = '1.5',course_id=cid).order_by('-score')     
    print(b)           
    data={
        "applicants":b,
        "course":c.course_name,
    }     
    return render(request,'ranklist.html',data)  

def sendinvite(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    applicants= request.POST.getlist('invite[]')
    if applicants==[]:
        return redirect('/ranklistview/') 
    cid=request.POST.get("cid")
    c=course.objects.get(id=cid)
    date=request.POST.get("date")  
    for i in applicants:
        a=application.objects.get(id=int(i))
        subject = 'Interview invitation'
        message = f'Welcome to EduExpert.\nApplicant name: {a.name}\nPhone: {a.phone}\nCourse: {c.course_name}\n\n\n The admission process has been scheduled on { date }. You are requested to reach the college by 9:00 am with the required documents.'
        email_from = cms.settings.EMAIL_HOST_USER
        recipient_list = [a.email]
        send_mail( subject, message, email_from, recipient_list )
        a.stage='2'
        a.save()
    return redirect('/ranklistview/')    

def courseapp2(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    c=course.objects.all()
    d=department.objects.all()
    data={
        "course":c,
        "dept":d,
    }
    return render(request,'courseapp2.html',data)

def appliview2(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    cid=request.POST.get("cid")
    cname=request.POST.get("cname")
    a=application.objects.filter(course_id=cid,stage='2')
    r=record.objects.all()
    data={
        "app":a,
        "rec":r,
        "course":cname,
    }
    return render(request,'appliview2.html',data)

def verify(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    cid=request.POST.get("cid")
    aid=request.POST.get("aid")
    app=application.objects.get(id=aid)
    #student admission
    s=student.objects.create(app_id=aid)
    s.save()
    app.stage="3"
    app.save()
    cname=request.POST.get("cname")
    a=application.objects.filter(course_id=cid,stage='2')
    r=record.objects.all()
    data={
        "app":a,
        "rec":r,
        "course":cname,
    }
    return render(request,'appliview2.html',data)

def newadmissions(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session.get("id")
    h=teacher.objects.get(login_id=id)
    dept=h.dept_id
    c=course.objects.filter(dept_id=dept)        
    data={
        "course":c,
    }                
   
    return render(request,'newadmissions.html',data)

def newadmissionview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    cid=request.POST.get("cid")
    id=request.session.get("id")
    h=teacher.objects.get(login_id=id)
    dept=h.dept_id
    c=course.objects.filter(dept_id=dept)
    ss=student.objects.filter(batch_id=0)
    stud=[]
    for sss in ss:
        stud.append(sss.app_id)
    a=application.objects.filter(stage='3',course_id=cid,pk__in=stud)
    finalapps=[]
    cs=[]
    for app in a:
        for i in c:
            if app.course_id == i.id:
                finalapps.append(app.id)
               
    ap=application.objects.filter(pk__in=finalapps)                    
    data={
        "app":ap,
        "course":c,
        "cname":course.objects.get(id=cid),
        "batch":batch.objects.filter(course_id=cid)
    }                

    return render(request,'newadmissionview.html',data)    

def batchadd(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session.get("id")    
    h=login.objects.get(id=id)
    hod=teacher.objects.get(login_id=id)
    dept_id=hod.dept_id
    c=course.objects.filter(dept_id=dept_id)
    l=login.objects.filter(utype_id__in=['2','3'],status='1')
    activeteachers=[]
    for ln in l:
        activeteachers.append(ln.id)       
    t=teacher.objects.filter(~Q(name='null'),dept_id=dept_id,login_id__in=activeteachers)
    data={
        "course":c,
        "teacher":t,
    }
    return render(request,'batchadd.html',data)   

def batchaddval(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    batch_id=request.POST.get("batch_id")
    num_class_in_week=request.POST.get("num_class_in_week")
    class_teacher=request.POST.get("class_teacher")
    course_id=request.POST.get("course_id")
    s=batch.objects.create(course_id=course_id,class_teacher=class_teacher,num_class_in_week=num_class_in_week,batch_id=batch_id)
    s.save()
    return redirect('/batchadd/')

def batchview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session.get("id")
    hod=teacher.objects.get(login_id=id)
    dept_id=hod.dept_id
    c=course.objects.filter(dept_id=dept_id)
    courses=[]
    for i in c:
        courses.append(i.id)
    batches=batch.objects.filter(course_id__in=courses)
    t=teacher.objects.filter(dept_id=dept_id)
    data={
        "batch":batches,
        "course":c,
        "teacher":t,
    }
    return render(request,'batchview.html',data)  

def addstudent(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    bid=request.POST.get("batch")
    sid= request.POST.getlist("students[]")
    if sid==[]:
        return redirect('/newadmissions/') 
    for s in sid:
        stud=student.objects.get(app_id=int(s))
        stud.batch_id=bid
        stud.save()
    return redirect('/newadmissions/')    

def subjectadd(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session.get("id")
    hod=teacher.objects.get(login_id=id)
    dept=hod.dept_id
    data={
        "deptid":dept,
    }     
    return render(request,'subjectadd.html',data)      



def subjectaddval(request):
    subject_number=request.POST.get("subject_number")
    subject_name=request.POST.get("subject_name")
    max_numb_students=request.POST.get("max_numb_students")
    subject_type=request.POST.get("subject_type")
    dept_id = request.POST.get("dept_id")
    s=subject.objects.create(subject_number=subject_number,subject_name=subject_name,subject_type=subject_type,max_numb_students=max_numb_students,dept_id=dept_id)
    s.save()
    return redirect('/subjectadd')

def subjectview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session.get("id")
    hod=teacher.objects.get(login_id=id)
    dept=hod.dept_id    
    sub=subject.objects.filter(dept_id=dept)
    c=course.objects.filter(dept_id=dept)
    data={
        "subjects":sub,
        "courses":c,
    }    
    return render(request,'subjectview.html',data)

def subjectedit(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    s=request.POST["subject_number"]    
    sub=subject.objects.get(subject_number=s)
    data={
        "subject":sub,
    }    
    return render(request,'subjectedit.html',data)

def subjectupdateval(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    subject_name=request.POST["subject_name"]
    subject_type=request.POST["subject_type"]
    max_numb_students=request.POST["max_numb_students"] 
    pk=request.POST["pk"]
    data=subject.objects.get(subject_number=pk)
    data.subject_name=subject_name
    data.subject_type=subject_type
    data.max_numb_students=max_numb_students
    data.save()
    return redirect('/subjectview')

def subjectaddcourse(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session.get("id")
    hod=teacher.objects.get(login_id=id)
    dept=hod.dept_id
    c=course.objects.filter(dept_id=dept)
    s=subject.objects.filter(dept_id=dept)
    data={
        "courses":c,
        "subjects":s,
    }
    return render(request,'subjectaddcourse.html',data) 

def subjectaddcourseval(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    course_id=request.POST.get("course_id")
    c=course.objects.get(id=course_id)
    subjects=request.POST.getlist("subject_id[]")
    
    for i in subjects:
        s=c.subjects.add(i)
    return redirect('/subjectaddcourse') 

def subjectcourseview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    c=course.objects.all()
    data={
        "courses":c,
    }    
    return render(request,'subjectcourseview.html',data)       

def subjectcourseedit(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    cid=request.POST["cid"]    
    c=course.objects.get(id=cid)
    s=subject.objects.all()
    data={
        "courses":c,
        "subjects":s,
    }
    return render(request,'subjectcourseedit.html',data)

def subjectcourseupdateval(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    cid=request.POST.get("cid")
    c=course.objects.get(id=cid)
    subj=request.POST.getlist("subject_id[]")
    sub=c.subjects.all()
    print(sub)
    for s in sub:
        if s.subject_number not in subj:                                                                                    
            s=c.subjects.remove(s)
    return redirect('/subjectcourseview')

def roomadd(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    return render(request,'roomadd.html') 

def roomview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    r = Room.objects.all() 
    data = {
        "rooms" : r,
    }   
    return render(request,'roomview.html',data)

def roomedit(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id = request.POST["id"]    
    r = Room.objects.get(id=id)
    data = {
        "room" : r,
    }
    return render(request,'roomeditview.html',data)

def roomupdateval(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id = request.POST["id"]
    room = Room.objects.get(id=id)
    room.r_number = request.POST["r_number"]
    room.seating_capacity = request.POST["seating_capacity"]
    room.save()
    return redirect('/roomview')

def roomaddval(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    r_number=request.POST.get("r_number")
    seating_capacity=request.POST.get("seating_capacity")
    s=Room.objects.create(r_number=r_number,seating_capacity=seating_capacity)
    s.save()
    return redirect('/roomadd')    

def meetingadd(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    hr=[]
    day=[]
    for i in time_slots:
        hr.append(i[0])  
    for i in DAYS_OF_WEEK:
        day.append(i[0])     
    data={
        "hours":hr,
        "da":day,
    }
    return render(request, 'meetingadd.html', data)

def meetingview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    meetings = MeetingTime.objects.all()        
    data={
        "hours":meetings,
     
    }
    return render(request, 'meetingview.html', data)

def meetingedit(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    pid=request.POST["pid"]    
    meeting = MeetingTime.objects.get(pid=pid) 
    hr=[]
    day=[]
    for i in time_slots:
        hr.append(i[0])  
    for i in DAYS_OF_WEEK:
        day.append(i[0])   
    data = {
        "hour":meeting,
        "days":day,
        "hours":hr,
        
    }
    return render(request, 'meetingeditview.html', data)

def meetingupdateval(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login') 
    pid=request.POST["pid"] 
    meeting = MeetingTime.objects.get(pid=pid) 
    meeting.time = request.POST["time"]  
    meeting.day = request.POST["day"]
    meeting.save()
    return redirect('/meetingview')  

def meetingaddval(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    pid=request.POST.get("pid")
    time=request.POST.get("time")
    day=request.POST.get("day")
    s=MeetingTime.objects.create(pid=pid, time=time, day=day)
    s.save()
    return redirect('/meetingadd')

def subjectaddteacher(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session.get("id")
    hod=teacher.objects.get(login_id=id)
    dept_id=hod.dept_id
    t=teacher.objects.filter(dept_id=dept_id)
    cid=request.POST.get("cid")    
    c=course.objects.get(id=cid)
    sub=c.subjects.all()
      
    data={
        "subjects":sub,
        "teachers":t,
    }
    print(data)
    return render(request,"subjectaddteacher.html",data)           

def subjectaddteacherval(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    subject_number=request.POST.get("subject_number")
    teacher_id=request.POST.getlist("teacher_id[]")
    s=subject.objects.get(subject_number=subject_number)
    for i in teacher_id:
        c=s.teachers.add(i)
    return redirect('/batchview')

def subjectteacherview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')    
    id=request.session.get("id")
    t = teacher.objects.get(login_id=id)
    sub = subject.objects.filter(dept_id=t.dept_id)
    tea = teacher.objects.filter(dept_id=t.dept_id)
    data = {
        "subjects":sub,
        "teachers":tea,
    }
    return render(request,"subjectteacherview.html",data)

def subjectteacheredit(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')    
    tid = request.POST["tid"]
    t = teacher.objects.get(id=tid)
    sub = subject.objects.filter(dept_id=t.dept_id)
    data = {
        "subjects" : sub,
        "teacher" : t,
    }
    return render(request,"subjectteacheredit.html",data)

def timetablegen(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    return render(request,"timetablegen.html")

def profile(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session.get("id")
    t = teacher.objects.get(login_id=id)
    d = department.objects.get(id=t.dept_id)
    data = {
        "hod" : t,
        "dept" : d,
    }
    return render(request,"profile.html",data)

def profileupdate(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session.get("id")    
    t = teacher.objects.get(login_id=id)
    t.name = request.POST["name"]
    t.dob = request.POST["dob"]
    t.gender = request.POST["gender"]
    t.address = request.POST["address"]
    t.email = request.POST["email"]
    t.phone = request.POST["phone"]
    t.qualification = request.POST["qualification"]
    if 'photo' not in request.FILES:
        t.save()
    else:
        Photo=request.FILES['photo']
        fs=FileSystemStorage()
        fn=fs.save(Photo.name, Photo)
        uploaded_file_url=fs.url(fn)
        t.photo=uploaded_file_url   
        t.save() 
    return redirect('/profile')

def teacherview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session['id']
    d=teacher.objects.get(id=id)
    dep=teacher.objects.filter(dept_id=d.dept_id)
    data={'teacher':dep,}
    return render(request, 'teacherview.html',data)

def teacherprofile(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session['id']
    t=teacher.objects.get(login_id=id)
    data={"t":t}
    return render(request, 'teacherprofile.html',data)

def teacherupdate(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session.get("id")    
    t = teacher.objects.get(login_id=id)
    t.name = request.POST["name"]
    t.dob = request.POST["dob"]
    t.gender = request.POST["gender"]
    t.address = request.POST["address"]
    t.email = request.POST["email"]
    t.phone = request.POST["phone"]
    t.qualification = request.POST["qualification"]
    if 'photo' not in request.FILES:
        t.save()
    else:
        Photo=request.FILES['photo']
        fs=FileSystemStorage()
        fn=fs.save(Photo.name, Photo)
        uploaded_file_url=fs.url(fn)
        t.photo=uploaded_file_url   
        t.save() 
    return redirect('/teacherprofile')

def studentview(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    id=request.session.get("id")
    b=batch.objects.get(class_teacher=id)
    s=student.objects.filter(batch_id=b.id)
    list=[]
    for i in s:
        a=application.objects.get(id=i.app_id)
        list.append(a)
    print(list)
    return render(request,'studentview.html',{'l':list})
