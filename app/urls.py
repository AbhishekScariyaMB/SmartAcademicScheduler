from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
     path('',views.home,name='home'),
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
 ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 