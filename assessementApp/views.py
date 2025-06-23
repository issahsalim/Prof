import os
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
import requests
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login ,logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
import smtplib 
from . task import * 
import csv 
from django.urls import reverse_lazy 
from django.template.loader import render_to_string 
from xhtml2pdf import pisa  
from django.contrib.auth.views import PasswordResetView 
from django.urls import reverse_lazy 
from django.contrib.auth import get_user_model  
import pandas as np  
import json 
from dotenv import load_dotenv
import math
# Create your views here.

load_dotenv() 
def base(request):
    return render(request,'base.html')

User= get_user_model() 

# CHECKING EMAIL WHEN RESETTING PASSWORD 
class CustomPasswordResetView(PasswordResetView):
    template_name = 'reset_password.html'
    email_template_name = "email_reset_password.html"
    success_url = reverse_lazy('password_reset_done')  

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        
        
        if User.objects.filter(email=email).exists():
          
            return super().form_valid(form)
        else:
           
            messages.error(self.request, "Email does not match any account")
            return self.form_invalid(form)
   
   
def home(request): 
    aboutinfo=About.objects.all()
    publication=Publications.objects.all()
    return render(request,'home.html',{'about':aboutinfo,'publications':publication}) 
                         

# def index(request):
#     return render(request,'index.html')

# SIGNUP
def register(request):
    if request.method == 'POST': 
        form =StudentForm(request.POST)
        if form.is_valid():   
                username=form.cleaned_data['username']
                telephone=form.cleaned_data['telephone']
                user = form.save(commit=False)   
                if CustomUser.objects.filter(telephone=telephone).exists:
                    messages.error(request,'An account with the same phone number already exist') 
                    return redirect('signup')
                if IndexNumbers.objects.filter(IndexNumbers=username).exists():
                    user.save() 
                    login(request, user) 
                    return redirect('home') 
                
                else: 
                    messages.error(request,"You are not allow to register please contact prof Appiahene")
                    return redirect('signup') 
    else:                                
        form = StudentForm()
    return render(request, 'register.html', {'form': form}) 
        # LOGIN



def loginForm(request):
    if request.method=='POST': 
                username=request.POST['username']
                password=request.POST['password'] 
                user= authenticate(username=username, password=password)

                if user is not None:    
                         login(request,user)
                         return redirect('home') 
                else:    

                    messages.error(request,'Invalid username or password')
                    return redirect('login')   
    
    return render(request,'login.html')  


# ADMIN 
def adminPage(request):
     if request.user.is_superuser:
        return render(request,'admin.html')
     messages.info(request,'You are not allow to access')
     return redirect('home')


# ANNOUNCEMENT
@login_required  
def announcement(request):  
     announcement=Announcement.objects.all()
     return render(request,'announcement.html',{'announcement':announcement})    

# UPLOADING RESULT  
@login_required 
def upload_results(request): 

    if request.method == "POST": 
        form = UploadResultForm(request.POST, request.FILES)
        
        if form.is_valid():
            save_result=form.save(commit=False)
            csv_file = form.cleaned_data.get('subject_file') 
            lecture_name=form.cleaned_data.get('lecture_name')
            Class =form.cleaned_data['Class']
            
            
            # CHECK IF TEACHER HAS ALREADY SUBMIT A CERTAIN SUBJECT 
            # if UploadResult.objects.filter(Class=Class).exists(): 
            #         messages.info(request,f'You have already submit {Class} result') 
            #         return redirect('upload_results') 
            

            # Check if the uploaded file is a valid CSV file
            csv_files=csv_file.content_type 
            if  csv_files!="text/csv":   
                messages.error(request, "Please upload a valid CSV file.")
                return redirect('upload_results')

            try:
                # Read and decode the file content
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                reader = csv.reader(decoded_file)
                
                # chek headers of the uploaded file 
                headers = next(reader)
                expected_headers = ['Index_number', 'Quizzes', 'Assignments', 'Level', 'Semester',"Total"] 
                if headers != expected_headers: 
                    messages.error(request, 'Please check the headers of your file.')
                    return redirect('upload_results')

                # Process the data to save to database
                for row in reader:
                    Result.objects.create(
                        index_number=row[0],
                        Quizzes=row[1],
                        Assignments=row[2], 
                        Level=row[3],
                        Semester=row[4],
                        Total=(float(row[1])+ float(row[2]) )
                    )   

                save_result.save() 
                messages.success(request, "Results uploaded successfully!")
                return redirect('upload_results')

            except Exception as e:  
                messages.error(request, f"An error occurred while processing the file: {str(e)}")
                return redirect('upload_results')

        else:
            # Form validation errors  
            messages.error(request, "Please correct the errors in the form.")
            return render(request, 'uploadResult.html', {'form': form})

    else:
        # Handle GET request
        form = UploadResultForm(
            initial={
                'lecture_name':request.user.username,
            }  
        )   
        submitted_course=UploadResult.objects.filter(lecture_name=request.user) 
    return render(request, 'uploadResult.html', {'form': form,'submitted_course':submitted_course,}) 
    


# DELETE SUBMITTED RESULT
def delete_result(request,result_id):
    getResultFromadmin=get_object_or_404(UploadResult, id=result_id) 
    getResultFromadmin.delete()  
    messages.info(request,'Result deleted')
    return redirect('upload_results')


# STUDENT RESULT 
@login_required
def student_results(request):
    recorded=Result.objects.filter(index_number=request.user).exists()
    if not recorded:    
        messages.info(request,f"{request.user.first_name} please your result has not been uploaded yet.")
        return redirect('home')

    results = Result.objects.filter(index_number=request.user).distinct() 
    return render(request, 'student_results.html', {'results': results})  


# DOWNLOADING RESULT 
@login_required
def downloadResult(request):
    # Fetch results for the logged-in user
    results = Result.objects.filter(index_number=request.user)  
    student = request.user
    
    # Path to the HTML template and context for rendering
    html_template = 'download_result.html' 
    context = {'results': results, 'student':student}
 
    # Render HTML as a string
    html = render_to_string(html_template, context) 

    # Prepare the HTTP response for PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={student.username}_result.pdf' 

    # Generate the PDF
    pisa_status = pisa.CreatePDF(html, dest=response) 

    # Check for errors during PDF generation
    if pisa_status.err: 
        return HttpResponse("An error occurred while downloading the results. Please try again.", content_type="text/plain")
    
    return response       



# ABSENCE
@login_required
def absence(request):
    error_message=None 
    student_full_name=f'{request.user.first_name} {request.user.last_name}'
 
    if request.method=="POST": 
        forms= AbsenceReport(request.POST,request.FILES )
        if forms.is_valid():  
            saveInfo=forms.save(commit=False)  
            indexNumber=forms.cleaned_data['stu_indexNumber']
            report_message=forms.cleaned_data['reason'] 
            if len(indexNumber)!=10:       
                messages.error(request,'Invalid Index Number')
                forms.save(commit=False)
                return redirect('absence')  
            
            saveInfo.save() 
            try: 
                admin_mail=[settings.EMAIL_HOST_USER] 
                report_mail=f"Report <{request.user.email}>" 
                send_mail( 
                     subject=f"Report from {student_full_name}",   
                     recipient_list= admin_mail,  
                     from_email= report_mail, 
                     message= f"Name:{student_full_name}\n Class:{request.user.Class}\n\n\n {report_message}",  
                     fail_silently=False 
                )  
                
            except BadHeaderError:
                 error_message="Bad response happen"

            except smtplib.SMTPException as e:
                 error_message=f"{e} but not worry your issue has been submitted"
            
            except Exception as e:
                 error_message=f"{e} but not worry your issue has been submitted" 

            if error_message:
                 messages.info(request,error_message) 
                 return redirect('absence')

            messages.success(request,f"Prof.Appiahene will hear from you, {student_full_name} wae")    
            return redirect('absence')     
    else:   
        absenceForm=AbsenceReport(
            initial={'stu_indexNumber': request.user.username,
                     'Class':request.user.Class, 'full_name':f'{student_full_name}'},
                                  )
                                         
        return render(request,'absence.html',{'absence_form':absenceForm}) 

# LOGOUT
def logoutFun(request): 
    logout(request) 
    messages.error(request,'Logout Successfully') 
    return redirect('index') 


# ASSESSMENT
# @login_required
# def Assessment(request):  
#     #   if request.user.is_authenticated:  
#          studentIndex=request.user.username 
#          if Assess_Student.objects.filter(index_Number=studentIndex).exists():
#             studentRecord=get_object_or_404(Assess_Student,index_Number=studentIndex) 
#             studentRecord.Total=(studentRecord.Total_Quiz_Marks + studentRecord.Total_Assignment_Mark + studentRecord.Attendance_Mark + studentRecord.Mid_Sem)/3
#             indexNumber=Assess_Student.objects.get(index_Number=studentIndex).index_Number
#             studentRecord.save()   
#             return redirect('Result',index=indexNumber) 
#          else:     
#              messages.error(request,'You have not been assess yet')  
#              return redirect('home') 
#     #   else:   
#     #       return redirect('home')  

@login_required  
def AssessmentDetail(request,index):  
   indexNumbers=get_object_or_404(Assess_Student, index_Number=index) 
   return render(request,'assessment.html',{'studentResult':indexNumbers}) 


def custom_404(request, exception):
    return render(request, '404.html', status=404) 


# ADD TA'S
def TA(request):
    teachers=FormMaster.objects.all()
    onpage={'teachers':teachers}
    
    return render(request,'formteacher.html',onpage)


@login_required 
def uploadIndexNumbers(request):
    if request.method=='POST': 
        form=indexNumbersForms(request.POST,request.FILES)
        if form.is_valid():  
            indexnumbers=request.FILES["file"] 
            # if not indexnumbers.name.endswith(".xls")

            # handling excel file 
            content_type=indexnumbers.content_type 
            if content_type=="application/vnd.ms-excel" : 
                df=np.read_excel(indexnumbers)
                if "Index Numbers" in df.columns:   
                    for indexnums in df["Index Numbers"]: 
                        IndexNumbers.objects.get_or_create(
                            IndexNumbers=str(indexnums)
                        )  
                    messages.info(request,'Uploaded Successfully') 
                    return redirect('uploadindex') 

                else:  
                    messages.error(request,"Please make sure your excel file has an index number column")
                    return redirect('uploadindex')
                
                # handling index number form csv file 
            elif content_type=="text/csv":
                df=np.read_csv(indexnumbers)
                if "Index Numbers" in df.columns:
                    for indexnums in df["Index Numbers"]:
                         IndexNumbers.objects.get_or_create(
                            IndexNumbers=str(indexnums)
                        )  
                    messages.info(request,'Uploaded Successfully') 
                    return redirect('uploadindex') 
                else:    
                    messages.error(request,"Please make sure csv file has an index number column")
                    return redirect('uploadindex')
                
            elif content_type=="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                df=np.read_excel(indexnumbers)
                if "Index Numbers" in df.columns:   
                    for indexnums in df["Index Numbers"]: 
                        IndexNumbers.objects.get_or_create(
                            IndexNumbers=str(indexnums)
                        ) 
                    messages.info(request,'Uploaded Successfully') 
                    return redirect('uploadindex') 

                else:  
                    messages.error(request,"Please make sure your excel file has an index number column")
                    return redirect('uploadindex')
            
            else: 
                messages.error(request,"Unsupported file format. Make sure it's csv or excel file")
                return redirect('uploadindex')  
        else: 
            messages.info(request,"Please upload a file !")
            return redirect('uploadindex') 

    else:
        form=indexNumbersForms()
        return render(request,'uploadIndexNumber.html',{'form':form})
            

# CHATBOT
def ChatBotView(request):
    chat=ChatBot.objects.filter(user=request.user).order_by('-created_at')

    if request.method=='POST':
         data = json.loads(request.body)
         userinput = data.get("message")

         try :
             payload = {
                "model": "meta-llama/llama-3.3-8b-instruct:free",
                "messages": [
                    {"role": "user", "content": userinput}
                ]
            } 

             headers = {
                "Authorization": f"Bearer {os.getenv('META_API')}", 
                          "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",   
                "X-Title": "My Chatbot"
            }

             response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
             result = response.json()
             
             ai_response = result["choices"][0]["message"]["content"] if "choices" in result else "No message received" 
             ChatBot.objects.create(user=request.user,userinput=userinput,ai_response=ai_response)
             return JsonResponse({"ai_response":ai_response})
             
         except Exception as e:  
            return JsonResponse({f"Error occur {str(e)}"},status=500) 
    else: 
        firstnameAlpha=request.user.first_name[:1]
        secondnameAlpha=request.user.last_name[:1]
        chats=ChatBot.objects.filter(user=request.user)
        return render(request,'test.html',{'chat':chat,'fn':firstnameAlpha,'sn':secondnameAlpha,'chatHis':chats})  


def chatHistoryView(request):
    chats=ChatBot.objects.filter(user=request.user)
    return render(request,'chatHistory.html',{'chatHis':chats})

def deleteChat(request,pk):
    chatdelete= get_object_or_404(ChatBot,pk=pk)
    chatdelete.delete()
    return redirect('Chatbot')
