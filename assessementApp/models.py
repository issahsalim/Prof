from django.db import models

# Create your models here.

from django.db import models
from django.forms import CharField 
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings 
import pandas as np
from django.utils.text import slugify 
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
# class Student(models.Model):
#     indexNumber= models.CharField(max_length=10)
#     Firstname=models.CharField(max_length=50)
#     Lastname=models.CharField(max_length=50)
#     phone=models.CharField(max_length=10)  
#     email=models.EmailField()
#     password=models.CharField(max_length=50)
#     c_password=models.CharField(max_length=50)
#     parentNumber=models.CharField(max_length=10) 
#     parent_mail=models.EmailField()   
#     def __str__(self):
#       return "{}   {}".format(self.Firstname,self.indexNumber)





class CustomUser(AbstractUser): 
    telephone = PhoneNumberField(region="GH") 
    Class= models.CharField(max_length=10,)

   
# class uploadIndexNumber(models.Model):
#    file=models.FileField(upload_to='indexnumbers')
   
#    def save(self, *args, **kwargs):
#      if self.file:
#         content_type=self.file.content_type 
#         if content_type=="application/vnd.ms-excel" : 
#                 df=np.read_excel(self.file)
#                 if "Index Numbers" in df.columns:   
#                     for indexnums in df["Index Numbers"]: 
#                         IndexNumbers.objects.get_or_create(
#                             IndexNumbers=str(indexnums)
#                         ) 
                      

#                 else:  
#                      raise ValueError("Please make sure csv file has an index number column")

                
#                 # handling index number form csv file 
#         elif content_type=="text/csv":
#                 df=np.read_csv(self.file)
#                 if "Index Numbers" in df.columns:
#                     for indexnums in df["Index Numbers"]:
#                          IndexNumbers.objects.get_or_create(
#                             IndexNumbers=str(indexnums)
#                         )  
                     
#                 else:    
#                   raise ValueError("Please make sure csv file has an index number column")
                
#         elif content_type=="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
#                 df=np.read_excel(self.file)
#                 if "Index Numbers" in df.columns:   
#                     for indexnums in df["Index Numbers"]: 
#                         IndexNumbers.objects.get_or_create(
#                             IndexNumbers=str(indexnums)
#                         )    

#                 else:  
#                     raise ValueError('Please make sure your excel file has an index number column')
            
#      super().save(*args,**kwargs)
   
class IndexNumbers(models.Model):
  IndexNumbers=models.CharField(max_length=10)

  class Meta:
      verbose_name="Index Number"
  def __str__(self): 
     return self.IndexNumbers
  


class Announcement(models.Model):
   title=models.CharField(max_length=200)
   message=models.TextField()
   date=models.DateTimeField()

   def __str__(self):
    return self.title 
    

class absenceReport(models.Model):
   stu_indexNumber=models.CharField(max_length=10)
   Class=models.CharField(max_length=10)  
   full_name=models.CharField(max_length=100)  
   reason=models.TextField(max_length=100)  
   proveFile=models.FileField(upload_to='upload', blank=True, null=True) 
   submitted_date=models.DateTimeField(auto_now_add=True)
   def __str__(self):
      return "{} - {}".format(self.stu_indexNumber,self.submitted_date)    


class Assess_Student(models.Model): 
    index_Number = models.CharField(max_length=10)   
    Total_Quiz_Marks = models.FloatField()
    Total_Assignment_Mark = models.FloatField()
    Attendance_Mark= models.FloatField() 
    Mid_Sem=models.FloatField()
    Total=models.FloatField(null=True, blank=True) 
     
    def __str__(self):
        return self.index_Number 


class studentResult(models.Model):
   index_number=models.CharField(max_length=10)
   Quizzes= models.IntegerField(default=0, editable=False)
   Assignments=models.IntegerField(default=0, editable=False)
   

class FormMaster(models.Model):
   name=models.CharField(max_length=100)
   phoneNumber= models.IntegerField(max_length=10)
   age=models.IntegerField()  
   picture= ProcessedImageField(
        upload_to='teachers',
        processors=[ResizeToFill(500, 500)],
        format='JPEG',
        options={'quality': 80}
    )   
   
   class Meta:
       verbose_name="Teaching Assistance"


# UPLOADING RESULTS TABLE
class UploadResult(models.Model):
   lecture_name=models.CharField(max_length=100)
   course=models.CharField(max_length=100) 
   Class=models.CharField(max_length=100)  
   subject_file=models.FileField(upload_to='ResultFiles')  
   uploaded_at=models.DateTimeField(auto_now=True) 

   class Meta:
      verbose_name="Uploaded Result" 
      



                     # RESULT

# STUDENT RESULT
class Result(models.Model):
    index_number = models.CharField(max_length=10)
    # slug=models.SlugField(blank=True)
    Quizzes = models.FloatField(default=0)
    Assignments= models.FloatField(default=0)
    Level = models.CharField(max_length=10)
    Total=models.FloatField(default=0,blank=True)
    Semester = models.CharField(max_length=50)   

    # def save(self,*args, **kwargs):
    #    self.slug=slugify(self.index_number)
    #    super().save(*args,**kwargs) 


    def __str__(self):       
        return f"{self.index_number} - {self.Level}- {self.Semester}"



# ABOUT INFO   
class About(models.Model):
   About_Message=models.TextField()
   readmore=models.CharField(max_length=100) 
   myimage=models.ImageField(upload_to='myimage') 
   
   class Meta:
       verbose_name="About Info"
       
   def __str__(self):
       return f"About me"
# PUBLICATIONS
class Publications(models.Model):
   publication_name=models.CharField(max_length=100)
   publication_number=models.IntegerField()
   publication_link=models.CharField(max_length=100)
   def __str__(self): 
     return self.publication_name 
   

# CHAT HISTORY 
class ChatBot(models.Model):
   user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE) 
   userinput=models.TextField()
   ai_response=models.TextField()
   created_at=models.DateTimeField(auto_now_add=True) 
   def __str__(self):
      return f" created by {self.user.username} at {self.created_at}" 
   