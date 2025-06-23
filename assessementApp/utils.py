# import firebase_admin 
# from firebase_admin import messaging

# def send_notification(token,title,message):
#     try:
#         notification= messaging.Message(
#             notification=messaging.Notification(
#                 title=title,
#                 body=message
#             ), 
#             token=token 
#         ) 
#         response=messaging.send(notification) 
#         print(f"Sent successfully {response}")
#     except Exception as e:
#         print(f"Error happen {e}") 
        