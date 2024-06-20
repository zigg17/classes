from tkinter import messagebox
from googletrans import Translator
import os
import csv
import customtkinter as CTk
from tkinter import messagebox
import pandas as pd

translator = Translator()

class Cycle:
    def __init__(self, iterable):
        self.items = iterable
        print(iterable)
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        item = self.items[self.index]
        self.index = (self.index + 1) % len(self.items)
        return item

    def prev(self):
        self.index = (self.index - 1) % len(self.items)
        return self.items[self.index]

    def current(self):
        return self.items[self.index]

class flashcard:
    def __init__(self, english_word: str, spanish_word: str):
        self.english_side = english_word
        self.spanish_side = spanish_word

class lexicon:
    def __init__(self, word_type: str):
        app_data_directory = os.path.join(os.path.expanduser('~'), 'spanData')

        # Create the directory if it doesn't exist
        os.makedirs(app_data_directory, exist_ok=True)

        # Define the filename
        filename = 'spanish.csv'

        # Define the full file path
        file_path = os.path.join(app_data_directory, filename)

        # Reading from save csv to pull data
        df = pd.read_csv(file_path)

        # Allows for users to go through entirety of word deck if they desire
        if(word_type != 'All'):
            df = df[df['Classification'] == word_type]
        else:
            df = df.drop(columns=['Classification'])

        # Saving first parts of the class
        self.english_words = list(df.iloc[:, 1])
        self.spanish_words = list(df.iloc[:, 0])
        
        # Converting class to flashcards
        self.flashcard_list = [flashcard(self.english_words[x], self.spanish_words[x]) for x in range(len(self.english_words))]

# Spanish translatore utilizing google translate
def spanTrans(text_to_translate):
    global translator
    translated_text = translator.translate(text_to_translate, dest = 'en', src = 'es')
    return translated_text.text

class spwords:
    def __init__(self, span, classification):
        self.span = span
        self.classification = classification
        self.eng = spanTrans(self.span)

        if (self.eng.lower() == self.span.lower()):
            messagebox.showerror(title = "Error", message = "Not translatable, misspelled, or both words are the same in both languages.")
            return

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

# Conversational flashcard window and operations
class convoflashcards(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.position_window(500, 400)
        self.title("JakeLingo: Conversational")
        
        # Initializes relevant words
        if(len(lexicon('Conversational').flashcard_list) == 0):
            messagebox.showerror(title = "Error", message = "No available words.")
            self.destroy()
            return
        else:
            convo_flashcards = Cycle(lexicon('Conversational').flashcard_list)

        # Create a frame to contain the buttons
        button_frame = CTk.CTkFrame(self)
        button_frame.pack(side="bottom", fill="x")

        # Initializes card frame
        card = CTk.CTkFrame(self, width=450, height=250, fg_color='white')
        card.place(x=26, y=45)

        # Add label to the card frame
        card_label = CTk.CTkLabel(card, text=convo_flashcards.current(), text_color='black', font=('Arial', 24))
        card_label.place(relx=0.5, rely=0.5, anchor="center")

        # Add buttons to the frame
        button1 = CTk.CTkButton(button_frame, text="Prev")
        button1.pack(side="left", padx=10, pady=10)
        button2 = CTk.CTkButton(button_frame, text="Next")
        button2.pack(side="left", padx=10, pady=10)
        button3 = CTk.CTkButton(button_frame, text="Flip")
        button3.pack(side="left", padx=10, pady=10)

    # Helps incorporate window in the proper place
    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

# Scientific flashcard window and operations
class scienceflashcards(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.position_window(500, 400)
        self.title("JakeLingo: Scientific")

        # Initializes relevant words
        if(len(lexicon('Scientific').flashcard_list) == 0):
            messagebox.showerror(title = "Error", message = "No available words.")
            self.destroy()
            return
        else:
            scientific_flashcards = Cycle(lexicon('Scientific').flashcard_list)
        
        # Create a frame to contain the buttons
        button_frame = CTk.CTkFrame(self)
        button_frame.pack(side="bottom", fill="x")

        card = CTk.CTkFrame(self, width=450, height=250, fg_color='white')
        card.place(x=26, y=45)

        # Add label to the card frame
        card_label = CTk.CTkLabel(card, text="Flashcard Text", text_color='black', font=('Arial', 24))
        card_label.place(relx=0.5, rely=0.5, anchor="center")

        # Add buttons to the frame
        button1 = CTk.CTkButton(button_frame, text="Prev")
        button1.pack(side="left", padx=10, pady=10)
        button2 = CTk.CTkButton(button_frame, text="Next")
        button2.pack(side="left", padx=10, pady=10)
        button3 = CTk.CTkButton(button_frame, text="Flip")
        button3.pack(side="left", padx=10, pady=10)

    # Positioning entire frame to be in proper place
    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

# Advanced flashcards window and operations
class advancedflashcards(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.position_window(500, 400)
        self.title("JakeLingo: Advanced")

        # Initializes relevant words
        if(len(lexicon('Advanced').flashcard_list) == 0):
            messagebox.showerror(title = "Error", message = "No available words.")
            self.destroy()
            return
        else:
            scientific_flashcards = Cycle(lexicon('Advanced').flashcard_list)
        
        # Create a frame to contain the buttons
        button_frame = CTk.CTkFrame(self)
        button_frame.pack(side="bottom", fill="x")

        card = CTk.CTkFrame(self, width=450, height=250, fg_color='white')
        card.place(x=26, y=45)

        # Add label to the card frame
        card_label = CTk.CTkLabel(card, text="Flashcard Text", text_color='black', font=('Arial', 24))
        card_label.place(relx=0.5, rely=0.5, anchor="center")

        # Add buttons to the frame
        button1 = CTk.CTkButton(button_frame, text="Prev")
        button1.pack(side="left", padx=10, pady=10)
        button2 = CTk.CTkButton(button_frame, text="Next")
        button2.pack(side="left", padx=10, pady=10)
        button3 = CTk.CTkButton(button_frame, text="Flip")
        button3.pack(side="left", padx=10, pady=10)

    # Positioning entire frame to be in the proper place
    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

# All flashcards window and operations
class allflashcards(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.position_window(500, 400)
        self.title("JakeLingo: All")

        # Initializes relevant words
        if(len(lexicon('All').flashcard_list) == 0):
            messagebox.showerror(title = "Error", message = "No available words.")
            self.destroy()
            return
        else:
            scientific_flashcards = Cycle(lexicon('All').flashcard_list)
        
        # Create a frame to contain the buttons
        button_frame = CTk.CTkFrame(self)
        button_frame.pack(side="bottom", fill="x")

        card = CTk.CTkFrame(self, width=450, height=250, fg_color='white')
        card.place(x=26, y=45)

        # Add label to the card frame
        card_label = CTk.CTkLabel(card, text="Flashcard Text", text_color='black', font=('Arial', 24))
        card_label.place(relx=0.5, rely=0.5, anchor="center")

        # Add buttons to the frame
        button1 = CTk.CTkButton(button_frame, text="Prev")
        button1.pack(side="left", padx=10, pady=10)
        button2 = CTk.CTkButton(button_frame, text="Next")
        button2.pack(side="left", padx=10, pady=10)
        button3 = CTk.CTkButton(button_frame, text="Flip")
        button3.pack(side="left", padx=10, pady=10)
    
    # Positioning the frame to be in the proper place
    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

# Add term class
class addterm(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        # Opening window for the add term page
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.position_window(300, 200)
        self.title("JakeLingo: Add Term")
        
        # Adding buffer label
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

    # Positioning window for better presentation
    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
    
    # Add word, check for an contingencies
    def addWord(self):
        # Error checking
        if self.entry.get() == '':
            messagebox.showerror("Error", "No entry for word")
            return
        if self.dropdown.get() == 'Word Type:':
            messagebox.showerror("Error", "Need word type.")
            return
        
        # The rest is for extracting string from custom tkinter interface
        spwords(span=str(self.entry.get()), classification=str(self.dropdown.get()))
        self.entry.delete(0,CTk.END)
        self.dropdown.set('Word Type:')
        self.update_idletasks()
        self.update()
        
# Final application to incorporate and run all of the code
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

        # File setup
        self.setup()

        # Create three frames with borders across the middle
        addButton = CTk.CTkButton(self, text="Add Term", command= lambda:self.open_term())
        addButton.place(x=200, y=390)

        addButton1 = CTk.CTkButton(self, text="Practice All", command= lambda:self.open_flashcards('all'))
        addButton1.place(x=450, y=390)

        # Conversational frame
        frame1 = CTk.CTkFrame(self, width=200, height=300, fg_color='white')
        frame1.place(x=50, y=50)
        label1 = CTk.CTkLabel(frame1, text="Conversational", text_color='black', font=("Helvetica", 12))
        label1.place(relx=0.5, rely=0.1, anchor='center')
        button1_flashcards = CTk.CTkButton(frame1, text="Flashcards",  command= lambda:self.open_flashcards('conversational'))
        button1_flashcards.place(relx=0.5, rely=0.4, anchor='center')
        button1_writing = CTk.CTkButton(frame1, text="Writing")
        button1_writing.place(relx=0.5, rely=0.6, anchor='center')

        # Scientific frame
        frame2 = CTk.CTkFrame(self, width=200, height=300, fg_color='white')
        frame2.place(x=300, y=50)
        label2 = CTk.CTkLabel(frame2, text="Scientific", text_color='black', font=("Helvetica", 12))
        label2.place(relx=0.5, rely=0.1, anchor='center')
        button2_flashcards = CTk.CTkButton(frame2, text="Flashcards",  command= lambda:self.open_flashcards('scientific'))
        button2_flashcards.place(relx=0.5, rely=0.4, anchor='center')
        button2_writing = CTk.CTkButton(frame2, text="Writing")
        button2_writing.place(relx=0.5, rely=0.6, anchor='center')

        # Advanced frame
        frame3 = CTk.CTkFrame(self, width=200, height=300, fg_color='white')
        frame3.place(x=550, y=50)
        label3 = CTk.CTkLabel(frame3, text="Advanced", text_color='black', font=("Helvetica", 12))
        label3.place(relx=0.5, rely=0.1, anchor='center')
        button3_flashcards = CTk.CTkButton(frame3, text="Flashcards",  command= lambda:self.open_flashcards('advanced'))
        button3_flashcards.place(relx=0.5, rely=0.4, anchor='center')
        button3_writing = CTk.CTkButton(frame3, text="Writing")
        button3_writing.place(relx=0.5, rely=0.6, anchor='center')
    
    # Responsible for setting up the directory if there isn't any
    def setup(self):
        spanDirectory = os.path.join(os.path.expanduser('~'), 'spanData')
        if not os.path.exists(spanDirectory):
            spwords('Español','Classification')
    
    # Postitioning of window opening for presentation
    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))  

    # Opens flashcards specefic to user inquery 
    def open_flashcards(self, button):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # Opens based on relevant strings coming in to the function
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
    
    # Responsible for opening the "add term window"
    def open_term(self):
        # Opens window if there isnt one already
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():   
            self.toplevel_window = addterm(self)  # create window if its None or destroyed
            self.toplevel_window.grab_set()
        else:
            self.toplevel_window.focus()  # if window exists focus it

# Final loop for application
if __name__ == "__main__":
    app = Application()
    app.mainloop()