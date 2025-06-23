from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin 
from django.contrib import admin, messages 
from django.core.mail import send_mass_mail,BadHeaderError
import smtplib 
from django.contrib.auth import get_user_model
# CUSTOMER USERS 
class CustomUserAdmin(UserAdmin):
    list_display=('username','first_name','last_name','Class','telephone','is_superuser' )  
    search_fields=('username','telephone','first_name','last_name') 
    
    fieldsets=(
        (None,{'fields':('username','password')}),
        ('Personal Info',{'fields':('telephone','first_name','last_name','Class','email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),

    )


    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'email','telephone', 'password1', 'password2', 'is_staff', 'is_active',),
    }),
)


    ordering=('username',) 

admin.site.register(CustomUser,CustomUserAdmin)
 


@admin.register(IndexNumbers)
class  studentIndeNumberAdmin(admin.ModelAdmin):
     search_fields=("IndexNumbers",)  

class AnnoucemetAdmin(admin.ModelAdmin):
    def save_model(self,request,obj,form,change):
        super().save_model(request,obj,form,change)

        try:
            title=obj.title 
            message=obj.message 
            from_mail=f"Prof <{settings.EMAIL_HOST_USER}>"  
            User=get_user_model() 
            recipient_mail=list(User.objects.values_list('email', flat=True))  
            if recipient_mail:
                send_mass_mail([  
                    (title,message,from_mail,recipient_mail) 
                ]) 
            self.message_user(request,"Action is successfully completed", level=message.SUCCESS) 
        
        except Exception as e:
             self.message_user(request, f"Announcement saved but email failed to send: {str(e)}", level=messages.ERROR)

        except BadHeaderError as e:
             self.message_user(request, f"Announcement saved but email failed to send: {str(e)}", level=messages.ERROR)

        except smtplib.SMTPException as e:
             self.message_user(request, f"Announcement saved but email failed to send: {str(e)}", level=messages.ERROR)


admin.site.register(Announcement,AnnoucemetAdmin)



@admin.register(absenceReport)
class AbsenceReportAdmin(admin.ModelAdmin):
    list_display=('stu_indexNumber','submitted_date',) 
    search_fields=("stu_indexNumber",)


@admin.register(FormMaster)
class Add_Form_Master(admin.ModelAdmin):
    list_display=('name','phoneNumber',)
    search_fields=("name","phoneNumber","age",)


# SUBMITTED RESULT 
@admin.register(UploadResult)
class ResultUploadAdmin(admin.ModelAdmin):
    list_display=('lecture_name','course','Class','uploaded_at',)
    search_fields=("course","Class",)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display=('index_number','Level','Semester',) 
    search_fields=("index_number","Level","Semester",) 

@admin.register(ChatBot)
class ChatbotAdmin(admin.ModelAdmin):
    list_display=('user','created_at',)
    search_fields=("user",)
# about admin
admin.site.register(About)
admin.site.register(Publications)

admin.site.site_header="Prof Appiahene"




