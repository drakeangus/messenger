import tkinter
#import tkinter.messagebox
import customtkinter
import os
import json
import threading
import time
import sys
from api_helpers import apirequests as api

print("[DEBUG] - Starting")

customtkinter.set_appearance_mode("dark")

class App(customtkinter.CTk):
    width = 1500
    height = 750

    corner_rad = 10

    local_sequence_number=0
    ScheduledEventsControl=False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("wtf is this")
        self.geometry(f"{self.width}x{self.height}")

        # Create login frame
        self.login_frame = customtkinter.CTkFrame(self,  corner_radius=10)
        
        self.login_frame.pack(pady=10, padx=10, fill="both", expand=True) 
        
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Login")
        self.login_label.pack(pady=12, padx=10)
        
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="Username")
        self.username_entry.pack(pady=12, padx=10)
        
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="Password")
        self.password_entry.pack(pady=12, padx=10)
        

        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.pack(pady=12, padx=10)
        


        # Create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=10)
        
        self.navigation_label = customtkinter.CTkLabel(self.navigation_frame, text="Navigation Frame")
        self.navigation_label.pack()
        
        #  button
        self.back_button = customtkinter.CTkButton(self.navigation_frame, text="DEBUG: Toggle Scheduled Events", command=self.test_event, width=200)
        self.back_button.pack(pady=12, padx=10)

        #  button
        #self.auto_update_messages_button = customtkinter.CTkCheckBox(self.navigation_frame, text="Auto update", command=self.auto_update_messages, width=200)
        #self.auto_update_messages_button = customtkinter.CTkButton(self.navigation_frame, text="Auto update", command=self.auto_update_messages, width=200)
        #self.auto_update_messages_button.pack(pady=12, padx=10)
        
        # Log out button
        self.back_button = customtkinter.CTkButton(self.navigation_frame, text="Log out", command=self.back_event, width=200)
        self.back_button.pack(pady=12, padx=10, side="bottom")



        # Create main frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=10)
        
        #self.main_label = customtkinter.CTkLabel(self.main_frame, text="Main Frame", font=customtkinter.CTkFont(size=20, weight="bold"))
        #self.main_label.pack()

        self.input_sub_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=5)
        self.message_sub_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=5)
        self.input_sub_frame.pack(pady=10, padx=10, fill="x", side="bottom")
        self.message_sub_frame.pack(pady=10, padx=10, fill="both", expand=True, side="top")
        
        
        
        # Create input box
        self.input_box = customtkinter.CTkEntry(self.input_sub_frame, corner_radius=10)
        self.input_box.pack(pady=10, padx=10, anchor="sw", fill="both", expand=True, side="left")
        self.input_box.bind('<Return>', self.send_event)
        self.send_button = customtkinter.CTkButton(self.input_sub_frame, text="Send", command=self.send_event, width=50)
        self.send_button.pack(pady=10, padx=10, anchor="se", side="right")
        
        # Create message sub frame
        self.message_box = customtkinter.CTkTextbox(self.message_sub_frame)
        self.message_box.configure(wrap="word") 
        self.message_box.pack(pady=10, padx=10, fill="both", expand=True)
        self.message_box.insert("10.10", "DEBUG: Start\n")

       
    

    def login_event(self):
        global username
        global ScheduledEventsControl
        username=self.username_entry.get()
        if username == "":
            username="UnknownUser"
        password=self.password_entry.get()
        print(f"Login Event: {username} / {password}")
        
        if username == "invalid":
            print("invlid user")

        if True or username == "angus" and password == "password": 
            self.login_frame.pack_forget()  # remove login frame
            
            self.navigation_frame.pack(pady=10, padx=10, side="left", fill="y", expand=False)
            self.main_frame.pack(pady=0, padx=0, side="right", fill="both", expand=True)
            
            self.populate_message_history()
            ScheduledEventsControl=True
            self.after(1000, self.ScheduledEvent)




    def populate_message_history(self):
        global local_sequence_number
        all_messages=api.get_all_messages()
        self.message_box.configure(state="normal")
        self.message_box.insert("end", "Unread messages : \n")
        for message_data in all_messages:
            self.message_box.insert("end", f'{message_data["user_id"]} : {message_data["message_text"]}\n')
            local_sequence_number = message_data['sequence_number']
        self.message_box.configure(state="disabled")
        self.message_box.see("end")
        
        
    def back_event(self):
        global ScheduledEventsControl
        print("Stop ScheduledEvents")
        ScheduledEventsControl=False
        self.navigation_frame.pack_forget()  # remove main frame
        self.main_frame.pack_forget()
        self.login_frame.pack(pady=10, padx=10, fill="both", expand=True)  # show login frame

    def CheckForNewMessages(self):
        global local_sequence_number
        remote_sequence_number = api.get_remote_sequence_number()
        if remote_sequence_number > local_sequence_number:
            print("THERE ARE UNREAD MESSAGES")
            
            new_messages = api.get_messages_in_range(local_sequence_number+1, remote_sequence_number)
            self.message_box.configure(state="normal")
            for message_data in new_messages:
                self.message_box.insert("end", f'{message_data["user_id"]} : {message_data["message_text"]}\n')
                local_sequence_number = message_data['sequence_number']
            self.message_box.configure(state="disabled")
            self.message_box.see("end")

    def ScheduledEvent(self):
        if ScheduledEventsControl == False:
            return
        #print("ScheduledEvent called")
        self.after(500, self.ScheduledEvent)
        self.CheckForNewMessages()
        

    def test_event(self):
        global local_sequence_number
        global ScheduledEventsControl
        if ScheduledEventsControl:
            print("Stop ScheduledEvents")
            ScheduledEventsControl=False
        else:
            print("Start ScheduledEvents")
            ScheduledEventsControl=True
            self.ScheduledEvent()


       
    def publish_message(self, sender, message):
        self.message_box.configure(state="normal")
        self.message_box.insert("end", f"{sender} : {message}\n")
        self.message_box.configure(state="disabled") # text box should be read-only after a message is published
        self.message_box.see("end")

   

    def send_event(self, *args):
        message=self.input_box.get()
        print(f"Message sending: {username} - {message}")
        
        self.input_box.delete(0, 'end') # clear input box

        user_id = 0
        api.send_new_message(user_id, message)
            
   
            
        
            


if __name__ == "__main__":
    app = App()
    app.mainloop()

    
