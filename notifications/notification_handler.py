
from winotify import Notification, audio

app_name = "Super secret chat"
#message_text = "Some text to inlcude in the notification, lets see what happens when it's quite long"
mungo = r"C:\Users\adrake\workspace\messenger\images\test_image.png"
face = r"C:\Users\adrake\workspace\messenger\images\face2.png"

'''
base_toast = Notification(app_id=app_name,
                     title="New Message Recieved",
                     msg=message_text,
                     duration="short",
                     )
'''

#toast_new_message.set_audio(audio.IM, loop=False)

#base_toast.show()

def NewMessage(sender, message_text, logo=face):
    if sender == "Mungo":
        logo=mungo
    toast_new_message = Notification(app_id=app_name,
                     title=f"New Message from {sender}",
                     msg=message_text,
                     duration="short",
                     icon=logo                   
                     )
    toast_new_message.set_audio(audio.IM, loop=False)
    toast_new_message.show()

