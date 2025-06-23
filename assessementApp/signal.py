# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Announcement,CustomUser 
# from django.core.mail import send_mass_mail,send_mail
# from django.conf import settings


# @receiver(post_save, sender=Announcement)  
# def admin_notify(sender, instance, created, **kwargs):  
#     if created:  
#         recipient_list=CustomUser.objects.filter(is_superuser=False).values_list('email',flat=True) 
#         from_mail=f"SchoolName <{settings.EMAIL_HOST_USER}>"
#         message=instance.message 
#         subject=instance.title  
        
#         send_mass_mail(
#             (subject,message,from_mail,[email]) 
#             for email in recipient_list 
#         )
    

