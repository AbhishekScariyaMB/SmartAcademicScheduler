from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
     path('',views.home,name='home'),
     path('depts/',views.depts),
     path('courses/',views.courses),
     path('login/',views.log_in,name='login'),
     path('dashboard/',views.user_login),
     path('teacher/',views.user_login),
     path('hod/',views.user_login),
     path('incharge/',views.user_login),
     path('login/',views.user_login),
     path('form-samples/',views.test_form),
     path('dashboardref/',views.dashboardref),
     path('deptadd/',views.deptadd),
     path('deptaddval/',views.deptaddval),
     path('deptview/',views.deptview),
     path('depteditview/',views.depteditview),
     path('deptedit/',views.deptedit),
     path('deptupdate/',views.deptupdate),
     path('logout/',views.logout),
     path('courseadd/',views.courseadd), 
     path('courseaddval/',views.courseaddval),
     path('courseview/',views.courseview),
     path('courseeditview/',views.courseeditview),
     path('courseedit/',views.courseedit),
     path('courseupdate/',views.courseupdate),
     path('useradd/',views.useradd),
     path('teacheradd/',views.teacheradd),
     path('admissionadd/',views.admissionadd),
     path('admissiongen/',views.admissiongen),
     path('teachergen/',views.teachergen),
     path('userview/',views.userview),
     path('usereditview/',views.usereditview),
     path('useredit/',views.useredit), 
     path('userupdate/',views.userupdate),     
     path('teacherregister/',views.teacherregister),
     path('sethod/',views.sethod),
     path('deptteacherview/',views.deptteacherview),
     path('hodupdate/',views.hodupdate), 
     path('hodview/',views.hodview), 
     path('appli/',views.appli),
     path('apply/',views.apply),
     path('courseapp/',views.courseapp),
     path('appliview/',views.appliview),
     path('confirmapp/',views.confirmapp),
     path('confirmedapp/',views.confirmedapp),
     path('ranklistview/',views.ranklistview),
     path('ranklist/',views.ranklist),
     path('sendinvite/',views.sendinvite),
     path('courseapp2/',views.courseapp2),
     path('appliview2/',views.appliview2),
     path('verify/',views.verify),
     path('newadmissions/',views.newadmissions),
     path('dash/',views.dash),
     path('dash2/',views.dash2),
     path('dash3/',views.dash3),
     path('dash4/',views.dash4),
     path('newadmissionview/',views.newadmissionview),
     path('batchadd/',views.batchadd),
     path('batchaddval/',views.batchaddval),
     path('batchview/',views.batchview),
     path('addstudent/',views.addstudent),
     path('subjectadd/',views.subjectadd),
     path('subjectview/',views.subjectview),
     path('subjectedit/',views.subjectedit),
     path('subjectupdateval/',views.subjectupdateval),
     path('subjectaddval/',views.subjectaddval),
     path('subjectaddcourse/',views.subjectaddcourse),
     path('subjectaddcourseval/',views.subjectaddcourseval),
     path('subjectcourseview/',views.subjectcourseview),
     path('subjectcourseedit/',views.subjectcourseedit),
     path('subjectcourseupdateval/',views.subjectcourseupdateval),
     path('roomadd/',views.roomadd),
     path('roomview/',views.roomview),
     path('roomedit/',views.roomedit),
     path('roomupdateval/',views.roomupdateval),
     path('roomaddval/',views.roomaddval),
     path('meetingadd/',views.meetingadd),
     path('meetingaddval/',views.meetingaddval),  
     path('meetingview/',views.meetingview),
     path('meetingedit/',views.meetingedit),
     path('meetingupdateval/',views.meetingupdateval),
     path('subjectaddteacher/',views.subjectaddteacher),
     path('subjectaddteacherval/',views.subjectaddteacherval),
     path('subjectteacherview/',views.subjectteacherview),
     path('subjectteacheredit/',views.subjectteacheredit),   
     path('timetable_generation/', views.timetable, name='timetable'),
     path('timetable/', views.timetablegen),
     path('profile/',views.profile),
     path('profileupdate/',views.profileupdate),
     path('teacherview/',views.teacherview),
     path('teacherprofile/',views.teacherprofile),
     path('teacherupdate/',views.teacherupdate),
     path('timetableview/',views.timetableview),
 ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 