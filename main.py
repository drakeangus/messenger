import tkinter
#import tkinter.messagebox
import customtkinter
import os
import json
import threading
import time
import sys

print("[DEBUG] - Starting")

customtkinter.set_appearance_mode("dark")

message_history_file = "message_history.json"
file_path = os.path.join(os.getcwd(), message_history_file)
if not os.path.exists(file_path):
    print("No message history file - exiting")
    exit()

check_new_messages=False

class App(customtkinter.CTk):
    width = 1500
    height = 750

    corner_rad = 10

    sequence_number=0

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
        self.back_button = customtkinter.CTkButton(self.navigation_frame, text="Check for new messages", command=self.test_event, width=200)
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

        self._stop_event = threading.Event()
        self._thread = None
    

    def login_event(self):
        global username
        global check_new_messages
        username=self.username_entry.get()
        if username == "":
            username="UnknownUser"
        password=self.password_entry.get()
        print(f"Login Event: {username} / {password}")

        if True or username == "angus" and password == "password": 
            self.login_frame.pack_forget()  # remove login frame
            
            self.navigation_frame.pack(pady=10, padx=10, side="left", fill="y", expand=False)
            self.main_frame.pack(pady=0, padx=0, side="right", fill="both", expand=True)
            
            self.populate_message_history()

            check_new_messages=True
            #self.auto_update_messages()


    def populate_message_history(self):
        global sequence_number
        file_path = os.path.join(os.getcwd(), message_history_file)
        self.message_box.configure(state="normal")
        if os.path.exists(file_path):
            self.message_box.insert("end", "Unread messages : \n")
            with open(file_path, 'r') as file:
                for line in file:
                    data = json.loads(line)
                    print(data)
                    sequence_number=data["SequenceNumber"]
                    sender=data["Sender"]
                    message=data["Message"]
                    self.message_box.insert("end", f"{sender} : {message}\n")
        else:
            print(f"File '{file_name}' does not exist in the current directory.")
            self.message_box.insert("end", "No message to display : \n")

        self.message_box.configure(state="disabled")
        
    def back_event(self):
        global check_new_messages
        check_new_messages=False
        self.navigation_frame.pack_forget()  # remove main frame
        self.main_frame.pack_forget()
        self.login_frame.pack(pady=10, padx=10, fill="both", expand=True)  # show login frame

    def test_event(self):
        print("Test button press")
        self.pull_new_messages()

    def pull_new_messages(self):
        global sequence_number
        remote_sequence = self.check_last_message_number()
        if  remote_sequence > sequence_number:
            for data in self.get_last_n_messages(remote_sequence - sequence_number):
                self.publish_message(data["Sender"], data["Message"])
            sequence_number = remote_sequence

    def publish_message(self, sender, message):
        self.message_box.configure(state="normal")
        self.message_box.insert("end", f"{sender} : {message}\n")
        self.message_box.configure(state="disabled") # text box should be read-only after a message is published
        self.message_box.see("end")

    def get_last_n_messages(self, n):
        last_n_entries = []
        # Form the full file path
        file_path = os.path.join(os.getcwd(), message_history_file)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                # Move the file pointer to the end of the file
                file.seek(0, 2)
                print("open file")
                pos = file.tell()
                count = 0
                while pos > 0 and count < n:
                    pos -= 1
                    file.seek(pos)
                    # Read a single byte
                    char = file.read(1)
                    # Check if it's a newline character
                    if char == b'\n':
                        # Move the pointer to the next position after newline
                        file.seek(pos + 1)
                        # Read and decode the last line
                        last_line = file.readline().decode('utf-8').strip()
                        # Load JSON data from the last line
                        last_entry = json.loads(last_line)
                        last_n_entries.insert(0, last_entry)  # Insert at the beginning to maintain order 
                        count += 1          
            return last_n_entries
            

    def check_last_message_number(self):
        data = self.get_last_n_messages(1)
        return data[0]["SequenceNumber"]

    def append_to_file(self, data):
        file_path = os.path.join(os.getcwd(), message_history_file)
        # Open the file in append mode
        with open(file_path, 'a') as file:
            # Write the JSON object to the file
            file.write('\n')
            json.dump(data, file)
            # Add a newline character to separate entries

    def send_event(self, *args):
        message=self.input_box.get()
        print(f"Message sending: {username} - {message}")
        
        self.input_box.delete(0, 'end') # clear input box

        # get last sequence number of file
        
        remote_sequence_number = self.check_last_message_number()
        # add new message with sequence number + 1
        new_seq_num = remote_sequence_number + 1
        new_json_message = {"SequenceNumber" : new_seq_num, "Sender" : username, "Message" : message}
        self.append_to_file(new_json_message)
            
        
    def auto_update_messages(self):
        if not self._thread or not self._thread.is_alive():    
            self._stop_event.clear()    
            self._thread = threading.Thread(target=self.update_new_messages())    
            self._thread.daemon = True    
            self._thread.auto_update_messages()
        
    def stop_auto_update_messages(self):    
        if self._thread and self._thread.is_alive():    
            self._stop_event.set()    
            self._thread.join()
            print("Stoppping updating with new messages")
    
    def update_new_messages(self):
        #threading.Timer(0.5, self.update_new_messages).start()
        time.sleep(1)
        while not self._stop_event.is_set():
            print(f"check time: {time.ctime()}")
            if check_new_messages:
                print("pull new messages")
                self.pull_new_messages()
            
        
            


if __name__ == "__main__":
    app = App()
    app.mainloop()

    app.stop_auto_update_messages()
