from tkinter import messagebox
from googletrans import Translator
import os
import csv
import customtkinter as CTk

translator = Translator()

def spanTrans(text_to_translate):
    global translator
    translated_text = translator.translate(text_to_translate, dest = 'en', src = 'es')
    return translated_text.text

class spwords:
    def __init__(self, span, classification):
        self.span = span
        self.classification = classification
        self.eng = spanTrans(self.span)

        app_data_directory = os.path.join(os.path.expanduser('~'), 'spanData')

        # Create the directory if it doesn't exist
        os.makedirs(app_data_directory, exist_ok=True)

        # Define the filename
        filename = 'spanish.csv'

        # Define the full file path
        file_path = os.path.join(app_data_directory, filename)

        # Write to the CSV file at the file path
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.span, self.eng, self.classification])

class convoflashcards(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.position_window(500, 400)
        self.title("JakeLingo: Conversational")
        
        # Create a frame to contain the buttons
        button_frame = CTk.CTkFrame(self)
        button_frame.pack(side="bottom", fill="x")

        card = CTk.CTkFrame(self, width = 450, height = 250 , fg_color= 'white')
        card.place(x= 26, y = 45)

        # Add buttons to the frame
        button1 = CTk.CTkButton(button_frame, text="Prev")
        button1.pack(side="left", padx=10, pady=10)
        button2 = CTk.CTkButton(button_frame, text="Next")
        button2.pack(side="left", padx=10, pady=10)
        button3 = CTk.CTkButton(button_frame, text="Flip")
        button3.pack(side="left", padx=10, pady=10)

    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

class scienceflashcards(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.position_window(500, 400)
        self.title("JakeLingo: Scientific")
        
        # Create a frame to contain the buttons
        button_frame = CTk.CTkFrame(self)
        button_frame.pack(side="bottom", fill="x")

        card = CTk.CTkFrame(self, width = 450, height = 250 , fg_color= 'white')
        card.place(x= 26, y = 45)

        # Add buttons to the frame
        button1 = CTk.CTkButton(button_frame, text="Prev")
        button1.pack(side="left", padx=10, pady=10)
        button2 = CTk.CTkButton(button_frame, text="Next")
        button2.pack(side="left", padx=10, pady=10)
        button3 = CTk.CTkButton(button_frame, text="Flip")
        button3.pack(side="left", padx=10, pady=10)

    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

class advancedflashcards(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.position_window(500, 400)
        self.title("JakeLingo: Advanced")
        
        # Create a frame to contain the buttons
        button_frame = CTk.CTkFrame(self)
        button_frame.pack(side="bottom", fill="x")

        card = CTk.CTkFrame(self, width = 450, height = 250 , fg_color= 'white')
        card.place(x= 26, y = 45)

        # Add buttons to the frame
        button1 = CTk.CTkButton(button_frame, text="Prev")
        button1.pack(side="left", padx=10, pady=10)
        button2 = CTk.CTkButton(button_frame, text="Next")
        button2.pack(side="left", padx=10, pady=10)
        button3 = CTk.CTkButton(button_frame, text="Flip")
        button3.pack(side="left", padx=10, pady=10)

    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
    

class allflashcards(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.position_window(500, 400)
        self.title("JakeLingo: All")
        
        # Create a frame to contain the buttons
        button_frame = CTk.CTkFrame(self)
        button_frame.pack(side="bottom", fill="x")

        card = CTk.CTkFrame(self, width = 450, height = 250 , fg_color= 'white')
        card.place(x= 26, y = 45)

        # Add buttons to the frame
        button1 = CTk.CTkButton(button_frame, text="Prev")
        button1.pack(side="left", padx=10, pady=10)
        button2 = CTk.CTkButton(button_frame, text="Next")
        button2.pack(side="left", padx=10, pady=10)
        button3 = CTk.CTkButton(button_frame, text="Flip")
        button3.pack(side="left", padx=10, pady=10)

    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

class addterm(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.position_window(300, 200)
        self.title("JakeLingo: Add Term")

        self.label = CTk.CTkLabel(self, text='')
        self.label.grid(row=0, column=0)

        # Text Entry
        self.entry = CTk.CTkEntry(self)
        self.entry.grid(row=1, column=0, padx=80, pady=10)

        # Dropdown (Combobox)
        self.dropdown = CTk.CTkComboBox(self, values=["Conversational", "Scientific", "Advanced"])  # Assuming you want a simple dropdown
        self.dropdown.grid(row=2, column=0, padx=10, pady=10)
        self.dropdown.set('Word Type:')

        # Button
        self.button = CTk.CTkButton(self, text="Submit", command= lambda: self.addWord())
        self.button.grid(row=3, column=0, padx=10, pady=20)

    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
    
    def addWord(self):
        if self.entry.get() == '':
            messagebox.showerror("Error", "No entry for word")
            return
        
        if self.dropdown.get() == 'Word Type:':
            messagebox.showerror("Error", "Need word type.")
            return
         
        spwords(span=str(self.entry.get()), classification=str(self.dropdown.get()))

        self.entry.delete(0,CTk.END)
        self.dropdown.set('Word Type:')
        self.update_idletasks()
        self.update()
        

class Application(CTk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize app settings
        CTk.set_appearance_mode('dark')
        self.title("JakeLingo")
        self.resizable(False, False)
        self.toplevel_window = None

        # Set the size of the window
        self.position_window(800, 450)

        # Filesetup
        self.setup()

        # Create three frames with borders across the middle
        addButton = CTk.CTkButton(self, text="Add Term", command= lambda:self.open_term())
        addButton.place(x=200, y=390)

        addButton1 = CTk.CTkButton(self, text="Practice All", command= lambda:self.open_flashcards('all'))
        addButton1.place(x=450, y=390)

        frame1 = CTk.CTkFrame(self, width=200, height=300, fg_color='white')
        frame1.place(x=50, y=50)
        label1 = CTk.CTkLabel(frame1, text="Conversational", text_color='black', font=("Helvetica", 12))
        label1.place(relx=0.5, rely=0.1, anchor='center')
        button1_flashcards = CTk.CTkButton(frame1, text="Flashcards",  command= lambda:self.open_flashcards('conversational'))
        button1_flashcards.place(relx=0.5, rely=0.4, anchor='center')
        button1_writing = CTk.CTkButton(frame1, text="Writing")
        button1_writing.place(relx=0.5, rely=0.6, anchor='center')

        frame2 = CTk.CTkFrame(self, width=200, height=300, fg_color='white')
        frame2.place(x=300, y=50)
        label2 = CTk.CTkLabel(frame2, text="Scientific", text_color='black', font=("Helvetica", 12))
        label2.place(relx=0.5, rely=0.1, anchor='center')
        button2_flashcards = CTk.CTkButton(frame2, text="Flashcards",  command= lambda:self.open_flashcards('scientific'))
        button2_flashcards.place(relx=0.5, rely=0.4, anchor='center')
        button2_writing = CTk.CTkButton(frame2, text="Writing")
        button2_writing.place(relx=0.5, rely=0.6, anchor='center')

        frame3 = CTk.CTkFrame(self, width=200, height=300, fg_color='white')
        frame3.place(x=550, y=50)
        label3 = CTk.CTkLabel(frame3, text="Advanced", text_color='black', font=("Helvetica", 12))
        label3.place(relx=0.5, rely=0.1, anchor='center')
        button3_flashcards = CTk.CTkButton(frame3, text="Flashcards",  command= lambda:self.open_flashcards('advanced'))
        button3_flashcards.place(relx=0.5, rely=0.4, anchor='center')
        button3_writing = CTk.CTkButton(frame3, text="Writing")
        button3_writing.place(relx=0.5, rely=0.6, anchor='center')
    
    def setup(self):
        spanDirectory = os.path.join(os.path.expanduser('~'), 'spanData')
        if not os.path.exists(spanDirectory):
            spwords('Español','Classification')
    
    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))  

    def open_flashcards(self, button):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            if button == 'all':
                self.toplevel_window = allflashcards(self)  # create window if its None or destroyed
                self.toplevel_window.grab_set()

            if button == 'conversational':
                self.toplevel_window = convoflashcards(self)  # create window if its None or destroyed
                self.toplevel_window.grab_set()
            
            if button == 'scientific':
                self.toplevel_window = scienceflashcards(self)  # create window if its None or destroyed
                self.toplevel_window.grab_set()
            
            if button == 'advanced':
                self.toplevel_window = advancedflashcards(self)  # create window if its None or destroyed
                self.toplevel_window.grab_set()

        else:
            self.toplevel_window.focus()  # if window exists focus it
    
    def open_term(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():   
            self.toplevel_window = addterm(self)  # create window if its None or destroyed
            self.toplevel_window.grab_set()
        else:
            self.toplevel_window.focus()  # if window exists focus it   

if __name__ == "__main__":
    app = Application()
    app.mainloop()