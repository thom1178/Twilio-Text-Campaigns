"""
This program creates a tkinter program, where a user can send a mass text message to a selected
group of people. The filtering in this file considers 'All Member', 'Non Members', 'Ind Members'
etc.. but it can be modified to fit a variety of purposes.


"""
from twilio.rest import Client
import pandas as pd
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import time


class build_gui:
    def __init__(self, master):
        # Your Account SID from twilio.com/console

        self.account_sid = "<Twilio account sid>"
        # Your Auth Token from twilio.com/console
        self.auth_token  = "<Twilio auth token>"
        
        self.client = Client(self.account_sid, self.auth_token)
        ###### Create GUI ######
        master.title("Example | Text Campaign")
        frame = tk.Frame()
        frame.pack()

        self.title_text_to_send = tk.Label(frame, text = "Send text message to Users: ").grid(row = 0, column =1, columnspan = 3)
        self.entry_message = tk.Text(frame,height = 3,width=40)
        self.entry_message.grid(row = 1, column = 1, columnspan = 3, rowspan = 2)
        self.test = tk.IntVar(value=1)
        self.button_state = ""
        self.all_cont = tk.Button(frame, text = "All  Contacts", command = lambda: self.whichContact("AC") , width = 20)
        self.orig_color = self.all_cont.cget("background")
        self.all_cont.grid(row = 0, column = 0)
        self.all_members = tk.Button(frame, text = "All  Members", command = lambda: self.whichContact("AM"), width = 20)
        self.all_members.grid(row = 1, column = 0)
        self.non_members = tk.Button(frame, text = "Non Members", command = lambda: self.whichContact("NM"), width = 20)
        self.non_members.grid(row = 2, column = 0)
        self.ind_members = tk.Button(frame, text = "Ind  Members", command = lambda: self.whichContact("IM"), width = 20)
        self.ind_members.grid(row = 3, column = 0)
        self.bus_members = tk.Button(frame, text = "Bus  Members", command = lambda: self.whichContact("BM"), width = 20)
        self.bus_members.grid(row = 4, column = 0)

        #Test users - use before sending
        self.title_test_users = tk.Label(frame, text = "Test users phone #").grid(row = 4, column =1, columnspan = 3)
        self.test_user1 = tk.Entry(frame)
        self.test_user1.grid(row = 5, column = 1)
        self.test_user1.insert(0, "<Test Phone Number>")
        self.test_user2 = tk.Entry(frame)
        self.test_user2.grid(row = 5, column = 2)
        #self.test_user2.insert(0, "562-351-9697")
        self.test_user3 = tk.Entry(frame)
        self.test_user3.grid(row = 5, column = 3)

        #Checkbox
        tk.Checkbutton(frame, text="Test", variable=self.test).grid(row=3, column = 2,columnspan = 1)
        
        self.submit = tk.Button(frame, text = "Submit",
                                command = lambda: self.send_message(cont = self.client,
                                                                    message_body = self.retrieve_text_input(),
                                                                    button_state = self.button_state,
                                                                    test = self.test.get(),
                                                                    testusers = self.retrieve_test_users())).grid(row=3,column=3)
        self.label_msg = tk.Label(frame, text = "")
        self.label_msg.grid(row=6, column = 0,columnspan = 4)
        self.choose_file = tk.Button(frame, text = "Choose File", command = self.file_picker , width = 20).grid(row=7, column = 0,columnspan = 1)
        self.chosen_file = tk.Label(frame, text = "No file chosen")
        self.chosen_file.grid(row = 8, column =0, columnspan = 4, sticky=tk.W)
        ######### End GUI ########
        root.minsize(200, 200)
        
    def clear_color(self):
        ##### This function clears button colors ########
        self.all_cont.configure(bg = self.orig_color)
        self.all_members.configure(bg = self.orig_color)
        self.non_members.configure(bg = self.orig_color)
        self.ind_members.configure(bg = self.orig_color)
        self.bus_members.configure(bg = self.orig_color)
        return
    
    def whichContact(self, to_contact):
        #### Filter Pandas DF ######
        self.button_state = to_contact
        self.clear_color()
        bg_color = "#e14d42"
        if "First Name" and "Mobile Phone" and "Member Type" and "Is Member" in self.contacts:
            if to_contact == "AC":
                self.all_cont.configure(bg = bg_color)
            elif to_contact == "AM":
                self.contacts_to_send = self.contacts.loc[self.contacts["Is Member"]== True]
                self.all_members.configure(bg = bg_color)
            elif to_contact == "NM":
                self.contacts_to_send = self.contacts.loc[self.contacts["Member Type"]== "NM"]
                self.non_members.configure(bg = bg_color)
            elif to_contact == "IM":
                self.contacts_to_send = self.contacts.loc[(self.contacts["Member Type"]== "HOH")|(self.contacts["Member Type"]== "HM")]
                self.ind_members.configure(bg = bg_color)
            elif to_contact == "BM":
                self.contacts_to_send = self.contacts.loc[self.contacts["Member Type"]== "BN"]
                self.bus_members.configure(bg = bg_color)
        return
        
    def retrieve_text_input(self):
        ##### Clear text when submission is finished ######
        inputValue=self.entry_message.get("1.0","end-1c")
        return(inputValue)
    
    def retrieve_test_users(self):
        ##### Get test users #######
        user_numbers = []
        if self.test_user1.get() is not None:
            user_numbers.append(self.test_user1.get())
        if self.test_user2.get() is not None:
            user_numbers.append(self.test_user2.get())
        if self.test_user3.get() is not None:
            user_numbers.append(self.test_user3.get())
        return(user_numbers)
    
    def send_all_dialog(self, num_contacts):
        ####### Are you sure you question box popup #####
        self.MsgBox = tkinter.messagebox.askquestion ('Send Text','Are you sure you want to send a text to all ' + str(num_contacts) + " contacts?",icon = 'warning')
        return(self.MsgBox)
    
    def file_picker(self):
        ######## Choose contacts file #########
        self.filename =  tkinter.filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
        self.contacts = pd.read_csv(self.filename)
        #Example Filtering
        if "First Name" and "Mobile Phone" and "Member Type" and "Is Member" in self.contacts:
            self.contacts = self.contacts.loc[self.contacts["Mobile Phone"].dropna().index]
            self.contacts_to_send = self.contacts.copy()
            self.chosen_file.config(text = str(self.filename))
        else:
            self.contacts = pd.DataFrame([])
            self.chosen_file.config(text = "File must contain the following columns: First Name, Last Name, Member Type and Is Member")
        return
    
    def send_message(self,cont, message_body, button_state, test = True, testusers = []):
        ######### Handle sending message ##########
        if message_body == "":
            return
        indx = 1
        if test == 1:
            num_sent = len([x for x in testusers if x != ""])
            to_send_value = self.send_all_dialog(num_sent)
            if to_send_value == 'yes': #Yes to send_all_dialog()
                for user in testusers:
                    if user == "":
                        continue
                    else:
                        try:
                            message = cont.messages.create(
                            to=user, 
                            from_="<Twilio Phone>",
                            body=message_body)
                            print("Sending: " + user)
                            time.sleep(1)
                        except Exception as e:
                            print(e)
            else:
                return

        else:
            num_sent = self.contacts_to_send.shape[0]
            to_send_value = self.send_all_dialog(num_sent)
            if to_send_value == 'yes':
                for x in range(self.contacts_to_send.shape[0]):
                    user = self.contacts.iloc[x,:]["Mobile Phone"]
                    if user == "":
                        continue
                    else:
                        
                        try:
                            message = cont.messages.create(
                            to=user, 
                            from_="<Twilio Phone>",
                            body=message_body)
                            #print("Sending: " + user)
                            time.sleep(1)
                        except Exception as e:
                            self.chosen_file.config(text = str(e))
                            
            else:
                return
        self.label_msg.config(text = "Message sent: " + message_body + " to users. \n" + str(num_sent) + " messages sent")
        self.entry_message.delete("1.0",tk.END)
        return
if __name__ == "__main__":
    root = tk.Tk()
    b = build_gui(root)
    root.mainloop()


