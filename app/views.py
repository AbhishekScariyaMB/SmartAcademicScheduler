from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from app.models import login , utype, department, course, teacher, application, parent, record
from django.contrib import messages
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
import cms.settings
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request,'home.html')

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
                    if e.name=='admin':
                        return render(request, 'dashboard.html',{"username":data.username})
                    elif e.name=='teacher':
                        dat3=teacher.objects.get(login_id=d.id)
                        if dat3.name=='null':
                            return render(request, 'teacherregister.html')
                        else:    
                            return render(request, 'teacher.html',{"username":dat3.name})  
                    elif e.name=='hod':
                        return render(request, 'hod.html',{"username":data.username})     
                    elif e.name=='admission':
                        return render(request, 'incharge.html',{"username":data.username})
                    else:
                        return render(request, 'login.html')         
    if flag==0:
        messages.error(request,'Username or Password is incorrect!')
        return redirect('/login/')         

def test_form(request):
    return render(request, 'form-samples.html')

def dashboardref(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    return render(request, 'dashboard.html')  

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
    dept=department.objects.create(name=name)
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
    c=course.objects.create(name=name,duration=duration,dept_id=dept_id)
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

def teachergen(request):
    if request.session.is_empty():
        messages.error(request,'Session has expired, please login to continue!')
        return HttpResponseRedirect('/login')
    email = request.POST['email'] 
    password = request.POST['password']
    dept_id = request.POST['dept_id']  
    data=login.objects.all()
    for d in data:
        if d.username == email:
            messages.warning(request, 'User already exists...!')
            return redirect('/useradd/')
    l=login.objects.create(username=email,password=password,utype_id=2,status='1')
    l.save()
    login_id=l.id
    t=teacher.objects.create(name='null',dob='2017-06-15',gender='null',address='null',email=email,dept_id=dept_id,qualification='null',login_id=login_id)
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
    id=request.POST.get('id')
    data1=login.objects.get(pk=id)    
    data2=utype.objects.all()
    data={
          'user':data1,
          'utype':data2,  
            }
    return render(request, 'useredit.html',data)

def userupdate(request):
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
    data2=department.objects.all()
    dat={
        
        "department":data2,
    }
    return render(request, 'sethod.html', dat)    

def deptteacherview(request):
    id=request.POST.get("id") 
    data=teacher.objects.filter(dept_id=id) 
    dat={
        "teacher":data,     
    } 
    return render(request,'deptteacherview.html',dat)

def hodupdate(request):
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