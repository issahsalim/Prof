from .models import CustomUser 


def identify_user(request):
    return{
        'is_student':request.user.is_authenticated and not request.user.is_superuser 
    }


