from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
from .views import CustomPasswordResetView

urlpatterns=[
     path('',views.home,name='home'),
     path('home',views.home,name='home'), 
     path('login',views.userSignin,name='login'),
     path('signup',views.signup,name='signup'),
     path('subject',views.addsubjects,name='subjects'),
     path('subject_list',views.subjectlist,name='subject_list'),
     path('logout',views.logout_views,name='logout')  ,
     path('delete_sub/<int:subject_id>',views.delete_subject,name='delete_subject'),
     
     path('edit_group/<int:group_pk>',views.edit_group,name='edit_group'), 
     
     path('addtask',views.task_view,name='addtask'), 
     path('schedule_study',views.schedule_study,name='schedule_study'), 
     path('study_session',views.studySession,name='study_session'), 
     path('edit_schedule/<int:pk>',views.edit_schedule,name="edit_schedule"), 
     path('delete_schedule/<int:s_id>/',views.deleteSchedule,name="delete_schedule"), 
     path('add_group',views.addGroup,name='add_group') , 
     path('list_groups',views.list_groups,name='list_groups') ,
     path('deletegroup',views.list_deleteGroup,name='deletegrouplist') ,
     path('delete_group/<int:group_id>/',views.delete_group,name='delete_group') , 
          
     path('due_date',views.checkDate,name='due_date'),
 
     # RESETTING PASSWORD PATHS
     path('password_reset/',CustomPasswordResetView.as_view(
         template_name='reset_password.html',
         email_template_name="email_reset_password.html", 
         html_email_template_name="email_reset_password.html",
     ),name='password_reset'),  
    
    
     path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(
         template_name="reset_password_done.html",
         
     ),name="password_reset_done"),

     path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
         template_name="reset_password_confirm.html"
     ),name="password_reset_confirm"),

     path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
          template_name="reset_password_complete.html"  
     ),name='password_reset_complete'),

    #  report group url
    path('group_report',views.Report_group_view,name="group_report")  ,
    
    
    path('studytime',views.studyTime,name='studytime') ,
    path('remainder',views.remainder,name='remainder'),

    # testimonial
    path('testimonial',views.TestimonialView,name='testimonial') 
    
]

