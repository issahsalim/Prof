from xml.dom import ValidationErr
from django import forms
from django.forms import ModelForm, ValidationError
# from pydantic import ValidationError
from .models import  *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from phonenumber_field.formfields import PhoneNumberField 
from phonenumber_field.widgets import PhoneNumberPrefixWidget 

    
class StudentForm(UserCreationForm): 
    telephone = PhoneNumberField( widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'+233123456789'}))

    password1= forms.CharField(
         widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password','id':'password'})
    )

    password2= forms.CharField(
         widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'confirm','id':'c_password'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name','Class' ,'email','telephone','password1','password2']  

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder':'Index number'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}), 
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'example@gamil.com'}), 
            'Class': forms.TextInput(attrs={'class':'form-control','placeholder':'Eg: L300 ITA'}), 
            # 'telephone': forms.TextInput(attrs={'class': 'form-control','placeholder':'Phone number'}, max_length=10, unique=True), 
        }


    def telephone(self):
         cleaned_data=super().clean()
         telephone=cleaned_data.get('telephone') 
         if CustomUser.objects.filter(telephone=telephone).exists():
              self.add_error('telephone',"An account with this number already exist")
         return cleaned_data 
    

class AbsenceReport(ModelForm):
    class Meta: 
        model=absenceReport
        fields=("stu_indexNumber","reason","proveFile","Class","full_name" )

        labels={
             
            'proveFile':'Prove File ',
            # 'name':''
        }

        widgets={
            'stu_indexNumber':forms.TextInput(attrs={'class':'form-control','maxlength':'10','placeholder':'Index Number',}),
            'full_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name',}),
            'Class':forms.TextInput(attrs={'class':'form-control','maxlength':'10','placeholder':'Class',}),
            'reason':forms.Textarea(attrs={'class':'form-control mt-4','placeholder':'Reason','style':'height:100px'}),  
            'proveFile':forms.FileInput() ,
        }


    def clan_HandleinvalidIndexNumber(self):
        stu_indexNumber=self.cleaned_data.get('stu_indexNumber') 
        if len(stu_indexNumber)!=10:
            raise ValidationErr("invalid phone number")
        return stu_indexNumber


# UPLOADING RESULT 
class UploadResultForm(ModelForm): 
    class Meta: 
          model= UploadResult 
          fields=("lecture_name","course","Class","subject_file")  
          
          widgets={
                'lecture_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Teachers name'}),
                'course':forms.TextInput(attrs={'class':'form-control','placeholder':'course'}), 
                'Class':forms.TextInput(attrs={'class':'form-control','placeholder':'Your class'}), 
                'subject_file':forms.FileInput(attrs={'class':'form-control'}),  
            }


    # def clean(self):
    #            cleaned_data= super().clean() 
    #            class_name=cleaned_data.get('Class')
    #            teacher_name=cleaned_data.get('teacher_name') 
    #            if UploadResult.objects.filter(Class=class_name).exists(): 
    #                 self.add_error('Class',f'Please you have already submit {class_name} result') 

    #            return cleaned_data 
                    
    
class FormMasterForms(forms.ModelForm):
    class Meta:
        model=FormMaster
        fields="__all__"

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control',}),
            'phoneNumber':forms.TextInput(attrs={'class':'form-control','max-length':'10'}),
            'age':forms.TextInput(attrs={'class':'form-control'}),
            'picture':forms.FileInput(attrs={'class':'form-control'})
            
        }


#UPload student index numebr
class indexNumbersForms(forms.Form):
    file=forms.FileField(required=True) 


class ChatBotForm(forms.Form):
     userinput=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ask anything'}) 
     