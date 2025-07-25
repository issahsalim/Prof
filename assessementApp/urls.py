from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
from .views import CustomPasswordResetView

urlpatterns = [
    
    path('', views.home, name='index'),   
    path('index', views.home, name='index'),   
    path('signup', views.register, name='signup'),
    path('login', views.loginForm, name='login'),
    path('home', views.home, name='home'),
    path('logout', views.logoutFun, name='logout'),
    path('announcement', views.announcement, name='announcement'),
    path('absence', views.absence, name='absence'),
    path('uploadindex', views.uploadIndexNumbers, name='uploadindex'), 
    path('admins/', views.adminPage, name='admin'),
    
    path('delete_result/<int:result_id>/',views.delete_result,name='delete_result') ,

    path('upload-results/', views.upload_results, name='upload_results'),
    
    path('Result/<str:index>', views.AssessmentDetail, name='Result'),

    path('my-results', views.student_results, name='student_results'),
        
    path('download_result/',views.downloadResult,name='download_result') ,

    path('form_teacher',views.TA,name="TA") ,
    path('Chatbot',views.ChatBotView,name="Chatbot") ,
    path('Chathistory',views.chatHistoryView,name="Chathistory") ,
    path('delete-chat/<int:pk>/', views.deleteChat, name='delete_chat'),

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

]


