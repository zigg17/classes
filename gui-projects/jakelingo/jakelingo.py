from tkinter import messagebox
from googletrans import Translator
import os
import csv
import customtkinter as CTk
from tkinter import messagebox
import pandas as pd
from spanishconjugator import Conjugator
import random
import glob
from tkinter import messagebox
from datetime import datetime

translator = Translator()

class Cycle:
    def __init__(self, iterable):
        self.items = iterable
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
    
    def add(self, item):
        self.items.append(item)

class flashcard:
    def __init__(self, english_word: str, spanish_word: str):
        self.english_side = english_word
        self.spanish_side = spanish_word

class verb_unit:
    def __init__(self, english_word: str, inf: str, yo: str,
                 tu: str, el_ella_ud: str, nosotros: str,
                 vosotros: str, ellos_ellas_uds: str):
        self.english_word = english_word
        self.inf = inf
        self.yo = yo
        self.tu = tu
        self.el_ella_ud = el_ella_ud
        self.nosotros  = nosotros
        self.vosotros = vosotros
        self.ellos_ellas_uds = ellos_ellas_uds

class lexicon:
    def __init__(self, word_type: str, verb_tense=None):
        app_data_directory = os.path.join(os.path.expanduser('~'), 'spanData')

        # Create the directory if it doesn't exist
        os.makedirs(app_data_directory, exist_ok=True)

        # Define the filename
        filename = 'spanish.csv'

        # Define the full file path
        file_path = os.path.join(app_data_directory, filename)

        # Reading from save csv to pull data
        df = pd.read_csv(file_path)

        if word_type == 'Verb':
            df = df[df['verb?'] == True]
            verb_objects = []
            for x in range(len(df)):
                conjugate_dict = Conjugator().conjugate(df.iloc[x, 0], verb_tense, 'indicative')
                if conjugate_dict:
                    english_word = df.iloc[x, 1]
                    inf = df.iloc[x, 0]
                    yo = conjugate_dict.get('yo', '').encode('latin1').decode('utf-8')
                    tu = conjugate_dict.get('tu', '').encode('latin1').decode('utf-8')
                    el_ella_ud = conjugate_dict.get('el/ella/usted', '').encode('latin1').decode('utf-8')
                    nosotros = conjugate_dict.get('nosotros', '').encode('latin1').decode('utf-8')
                    vosotros = conjugate_dict.get('vosotros', '').encode('latin1').decode('utf-8')
                    ellos_ellas_uds = conjugate_dict.get('ellos/ellas/ustedes', '').encode('latin1').decode('utf-8')
                    verb_objects.append(verb_unit(english_word, inf, yo, tu,
                                                  el_ella_ud, nosotros,
                                                  vosotros, ellos_ellas_uds))
            self.verb_objects = verb_objects

        # Allows for users to go through entirety of word deck if they desire
        if word_type != 'All':
            df = df[df['Classification'] == word_type]
        else:
            df = df.drop(columns=['Classification'])

        # Saving first parts of the class
        self.english_words = list(df.iloc[:, 1])
        self.spanish_words = list(df.iloc[:, 0])

        # Converting class to flashcards
        self.flashcard_list = [flashcard(self.english_words[x],
                                         self.spanish_words[x]) for x in range(len(self.english_words))]
        
class library: 
    def __init__ (self, category):
        app_data_directory = os.path.join(os.path.expanduser('~'), 'spanData')
        if not os.path.exists(app_data_directory):
            os.makedirs(app_data_directory)
        library_directory = os.path.join(app_data_directory, 'library')
        if not os.path.exists(library_directory):
            os.makedirs(library_directory)
        convo_directory = os.path.join(library_directory, 'conversational')
        if not os.path.exists(convo_directory):
            os.makedirs(convo_directory)
        scientific_directory = os.path.join(library_directory, 'scientific')
        if not os.path.exists(scientific_directory):
            os.makedirs(scientific_directory)
        advanced_directory = os.path.join(library_directory, 'advanced')
        if not os.path.exists(advanced_directory):
            os.makedirs(advanced_directory) 
        
        directory = ''
        if category == 'convo':
            directory = convo_directory
        elif category == 'science':
            directory = scientific_directory
        elif category == 'advanced':
            directory = advanced_directory
        else:
            return
        
        self.file_paths = glob.glob(os.path.join(directory, '*'))

        self.error = False
        if not self.file_paths:
            messagebox.showerror("Error", "No files found in the directory.")
            self.error = True
            return
        
        self.file_paths = []
        # Loop through files in the directory and add their paths to the list
        for file_path in glob.glob(os.path.join(directory, '*')):
            self.file_paths.append(file_path)
        
        # List to hold file contents
        self.file_contents = []

        # Loop through each file path and read the content into a string
        for file_path in self.file_paths:
            with open(file_path, 'r') as file:
                data = file.read()
                self.file_contents.append(data)

class writing_entry:
    def __init__(self, title, text):
        self.title = title
        self.text = text

class portfolio:
    def __init__(self, category):
        app_data_directory = os.path.join(os.path.expanduser('~'), 'spanData')
        if not os.path.exists(app_data_directory):
            os.makedirs(app_data_directory)
        library_directory = os.path.join(app_data_directory, 'portfolio')
        if not os.path.exists(library_directory):
            os.makedirs(library_directory)
        convo_directory = os.path.join(library_directory, 'conversational')
        if not os.path.exists(convo_directory):
            os.makedirs(convo_directory)
        scientific_directory = os.path.join(library_directory, 'scientific')
        if not os.path.exists(scientific_directory):
            os.makedirs(scientific_directory)
        advanced_directory = os.path.join(library_directory, 'advanced')
        if not os.path.exists(advanced_directory):
            os.makedirs(advanced_directory)
        
        self.directory = ''
        if category == 'convo':
            self.directory = convo_directory
        elif category == 'science':
            self.directory = scientific_directory
        elif category == 'advanced':
            self.directory = advanced_directory
        else:
            return
        
        self.entries = []
        
        # Loop through files in the directory, add paths to the list, and read their contents
        for file_path in glob.glob(os.path.join(self.directory, '*')):
            with open(file_path, 'r') as file:
                data = file.read()
            self.entries.append(writing_entry(file_path, data))
        
        self.entries.sort(key=lambda entry: datetime.strptime(os.path.basename(entry.title),
                                                              '%m-%d-%Y_%I-%M-%S%p.txt'))

# Spanish translatore utilizing google translate
def spanTrans(text_to_translate):
    global translator
    translated_text = translator.translate(text_to_translate, dest = 'en', src = 'es')
    return translated_text.text

class spwords:
    def __init__(self, span, classification, verb):
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

        if(verb == True):
            self.eng = 'to ' + self.eng

        # Write to the CSV file at the file path
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.span, self.eng, self.classification, verb])

class FlashcardsWindow(CTk.CTkToplevel):
    def __init__(self, category, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.position_window(500, 400)
        self.title(f"JakeLingo: {title}")

        lexico = lexicon(category)

        # Initializes relevant words
        if len(lexico.flashcard_list) == 0:
            messagebox.showerror(title="Error", message="No available words.")
            self.destroy()
            return
        else:
            self.flashcards = Cycle(random.sample(lexico.flashcard_list, len(lexico.flashcard_list)))

        # Create a frame to contain the buttons
        self.button_frame = CTk.CTkFrame(self)
        self.button_frame.pack(side="bottom", fill="x")

        # Initializes card frame
        self.card = CTk.CTkFrame(self, width=450, height=250, fg_color='white')
        self.card.place(x=26, y=45)

        # Add label to the card frame
        self.card_label = CTk.CTkLabel(self.card, text=self.flashcards.current().spanish_side,
                                       text_color='black', font=('Arial', 24))
        self.card_label.place(relx=0.5, rely=0.5, anchor="center")

        # Add buttons to the frame
        self.button1 = CTk.CTkButton(self.button_frame, text="Prev", command=self.show_prev_card)
        self.button1.pack(side="left", padx=10, pady=10)
        self.button2 = CTk.CTkButton(self.button_frame, text="Next", command=self.show_next_card)
        self.button2.pack(side="left", padx=10, pady=10)
        self.button3 = CTk.CTkButton(self.button_frame, text="Flip", command=self.flip_card)
        self.button3.pack(side="left", padx=10, pady=10)

    # Helps incorporate window in the proper place
    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    # Function to show previous card
    def show_prev_card(self):
        self.flashcards.prev()
        self.card_label.configure(text=self.flashcards.current().spanish_side)

    # Function to show next card
    def show_next_card(self):
        self.flashcards.next()
        self.card_label.configure(text=self.flashcards.current().spanish_side)

    # Function to flip the card
    def flip_card(self):
        if self.card_label.cget("text") == self.flashcards.current().spanish_side:
            self.card_label.configure(text=self.flashcards.current().english_side)
        else:
            self.card_label.configure(text=self.flashcards.current().spanish_side)

# Usage example:
def open_flashcards_window(category):
    titles = {
        'conversational': 'Conversational',
        'scientific': 'Scientific',
        'advanced': 'Advanced',
        'all': 'All'
    }
    FlashcardsWindow(category=category.capitalize(), title=titles[category])

class VerbTenseSelectionWindow(CTk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.resizable(False, False)
        self.position_window(300, 155)
        self.title("Select Verb Tense")

        tenses = ['present', 'preterite', 'imperfect', 'future']
        for i, tense in enumerate(tenses):
            button = CTk.CTkButton(self, text=tense.capitalize(), command=lambda t=tense: self.select_tense(t))
            button.pack(pady=5, padx=10, fill="x")

    def select_tense(self, tense):
        self.parent.verb_tense = tense
        self.destroy()
        GridEntryWindow(verb_tense=tense)

    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

class ReadingTopLevel(CTk.CTkToplevel):
    def __init__(self, category, title):
        super().__init__()
        self.title(f"JakeLingo: {title}")
        self.position_window(700, 550)
        self.grab_set()
        self.resizable(False, False)

        libruh = library(category)
        if libruh.error:
            self.destroy()
            return
        
        self.title_strings = Cycle(random.sample(libruh.file_paths, len(libruh.file_paths)))
        self.paragraph_strings = Cycle(random.sample(libruh.file_contents, len(libruh.file_contents)))
        
        # Create a frame to contain the reading content
        self.content_frame = CTk.CTkFrame(self)
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.content_label = CTk.CTkLabel(self.content_frame, text=self.title_strings.current().split("/")[-1],
                                          font=("Arial", 14))
        self.content_label.pack(pady=10, padx=10)
        
        self.content_text = CTk.CTkTextbox(self.content_frame, wrap='word', height=350, width=580)
        self.content_text.insert('1.0', self.paragraph_strings.current())
        self.content_text.configure(state='disabled')
        self.content_text.pack(pady=10, padx=10)

        # Navigation and Add Term buttons frame
        self.button_frame = CTk.CTkFrame(self)
        self.button_frame.pack(side='bottom', fill='x', pady=10)
        
        # Left button
        self.left_button = CTk.CTkButton(self.button_frame, text="Previous", command=lambda: self.navigate_to_previous())
        self.left_button.place(relx=0.2, rely=0.5, anchor='center')
        
        # Add Term button
        self.add_term_button = CTk.CTkButton(self.button_frame, text="Add Term", command=lambda: self.open_add_term_window())
        self.add_term_button.place(relx=0.5, rely=0.5, anchor='center')
        
        # Right button
        self.right_button = CTk.CTkButton(self.button_frame, text="Next", command=lambda: self.navigate_to_next())
        self.right_button.place(relx=0.8, rely=0.5, anchor='center')
        
    def navigate_to_previous(self):
        self.title_strings.prev()
        self.content_label.configure(text = self.title_strings.current().split("/")[-1])
        
        self.paragraph_strings.prev()
        self.content_text.configure(state='normal')
        self.content_text.delete('1.0', 'end')
        self.content_text.insert('1.0', self.paragraph_strings.current())
        self.content_text.configure(state='disabled')
        
    def navigate_to_next(self):
        # Implement the navigation to the next entry
        self.title_strings.next()
        self.content_label.configure(text = self.title_strings.current().split("/")[-1])

        self.paragraph_strings.next()
        self.content_text.configure(state='normal')
        self.content_text.delete('1.0', 'end')
        self.content_text.insert('1.0', self.paragraph_strings.current())
        self.content_text.configure(state='disabled')
        
    def open_add_term_window(self):
        # Implement the functionality to open the add term window
        self.toplevel_window = addterm(self)  # create window if its None or destroyed
        self.toplevel_window.grab_set()

    # Helps incorporate window in the proper place
    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

def open_reading_window(category):
    titles = {
        'convo': 'Conversational',
        'science': 'Scientific',
        'advanced': 'Advanced',
    }
    ReadingTopLevel(category=category, title=titles[category])


class WritingTopLevel(CTk.CTkToplevel):
    def __init__(self, category, title):
        super().__init__()
        self.title(f"JakeLingo: {title}")
        self.position_window(560, 450)
        self.grab_set()
        self.resizable(False, False)
        self.journal_entries_window = None  # Initialize the attribute
        self.portafolio = portfolio(category)
        self.current_index = len(self.portafolio.entries) - 1  # Start at the most recent entry

        # Configure grid columns and rows
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)

        # Add title label at the top
        self.title_label = CTk.CTkLabel(self, text='No Entries', font=("Helvetica", 16))
        self.title_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Add text box in the middle
        self.text_box = CTk.CTkTextbox(self, height=20)
        self.text_box.grid(row=1, column=0, rowspan=3, columnspan=4, padx=20, pady=10, sticky='nsew')

        # Add buttons at the bottom
        self.left_button = CTk.CTkButton(self, text="prev", command=self.navigate_to_previous)
        self.left_button.grid(row=4, column=0, pady=15, sticky='ew')

        self.right_button = CTk.CTkButton(self, text="next", command=self.navigate_to_next)
        self.right_button.grid(row=4, column=1, pady=15, sticky='ew')

        self.journal_search_button = CTk.CTkButton(self, text="Search By Date", command=self.open_journal_entries_popup)
        self.journal_search_button.grid(row=4, column=2, pady=15, sticky='ew')

        self.new_entry_button = CTk.CTkButton(self, text="New Entry", command=lambda: self.create_journal_popup(category))
        self.new_entry_button.grid(row=4, column=3, pady=15, sticky='ew')

        if self.portafolio.entries:
            self.load_writing(self.current_index)
        else:
            messagebox.showerror("Error", "No entries found.")

    # Helps incorporate window in the proper place
    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def open_journal_entries_popup(self):
        # Create a new top-level window for journal entries
        flag = False
        if len(self.portafolio.entries) == 0:
            messagebox.showerror("Error", "No entries.")
            return
        else:
            flag = True

        self.journal_entries_window = CTk.CTkToplevel(self)
        self.journal_entries_window.geometry("+{}+{}".format(self.winfo_rootx() + 100, self.winfo_rooty() + 75))
        self.journal_entries_window.title("Journal Entries")

        # Set the popup as a modal window
        self.journal_entries_window.grab_set()

        # Use a scrollable frame to accommodate a large number of entries
        scrollable_frame = CTk.CTkScrollableFrame(self.journal_entries_window)
        scrollable_frame.pack(fill='both', expand=True)

        if flag:
            for index, entry in enumerate(self.portafolio.entries):
                entry_date = entry.title.split('/')[-1].split('.')[0]
                date_button = CTk.CTkButton(scrollable_frame, text=entry_date,
                                            command=lambda idx=index: self.load_writing(idx))
                date_button.pack(pady=5, padx=10, fill='x')

    def load_writing(self, index):
        if index < 0 or index >= len(self.portafolio.entries):
            return

        self.current_index = index
        entry = self.portafolio.entries[index]
        file_path = entry.title
        with open(file_path, 'r') as file:
            file_content = file.read()

        self.title_label.configure(text='Entry at: ' + entry.title.split('/')[-1].split('.')[0])

        self.text_box.configure(state='normal')
        self.text_box.delete('1.0', 'end')
        self.text_box.insert('1.0', file_content)
        self.text_box.configure(state='disabled')

        if self.journal_entries_window is not None and self.journal_entries_window.winfo_exists():
            self.journal_entries_window.destroy()

    def navigate_to_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_writing(self.current_index)

    def navigate_to_next(self):
        if self.current_index < len(self.portafolio.entries) - 1:
            self.current_index += 1
            self.load_writing(self.current_index)
        

    def create_journal_popup(self, category):
        # Create a new top-level window
        self.journal_window = CTk.CTkToplevel(self)
        self.journal_window.title("Journal Entry")
        self.journal_window.grab_set()
        self.resizable(False, False)

        # Position the new window relative to the main window
        self.journal_window.geometry("+{}+{}".format(self.winfo_rootx() + 100, self.winfo_rooty() + 75))

        # Create a text entry box
        self.journal_entry = CTk.CTkTextbox(self.journal_window, height=300, width=500, wrap='word')
        self.journal_entry.pack(padx=10, pady=10)

        # Create a submit button
        submit_button = CTk.CTkButton(self.journal_window, text="Submit", command=lambda: self.submit_journal_entry(category))
        submit_button.pack(pady=10)

    def submit_journal_entry(self, category):
        # Get text from the text entry box
        journal_text = self.journal_entry.get("1.0", "end-1c")

        # Ask for confirmation
        if messagebox.askyesno("Confirm", "Are you sure you want to submit?"):
            # Get the current date and time
            now = datetime.now()
            filename = now.strftime("%m-%d-%Y_%I-%M-%S%p") + '.txt'
            full_file = os.path.join(self.portafolio.directory, filename)
            with open(full_file, 'w') as file:
                file.write(journal_text)
            self.journal_window.destroy()
            self.portafolio = portfolio(category)  # Refresh the portfolio to include the new entry
            self.current_index = len(self.portafolio.entries) - 1  # Reset the index to the most recent entry
            self.load_writing(self.current_index)  # Load the most recent entry

def open_writing_window(category):
    titles = {
        'convo': 'Conversational',
        'science': 'Scientific',
        'advanced': 'Advanced',
    }
    WritingTopLevel(category=category, title=titles[category])



class GridEntryWindow(CTk.CTkToplevel):
    def __init__(self, verb_tense='present'):
        super().__init__()
        self.verb_tense = verb_tense
        self.resizable(False, False)
        self.position_window(500, 300)
        self.title(f"JakeLingo: Verb Practice ({verb_tense.capitalize()})")

        self.verb_list = Cycle(random.sample(lexicon('Verb', verb_tense).verb_objects, 
                                  len(lexicon('Verb', verb_tense).verb_objects)))

        # Add a label on top of the grid
        self.top_label = CTk.CTkLabel(self, text=f"{self.verb_list.current().inf}", text_color='white', font=('Arial', 16))
        self.top_label.pack(pady=10)

        # Create a frame for the 3x2 grid of entry boxes
        self.grid_frame = CTk.CTkFrame(self)
        self.grid_frame.pack(pady=20)

        # Create a 3x2 grid of entry boxes
        self.entries = []
        for row in range(3):
            row_entries = []
            for col in range(2):
                entry = CTk.CTkEntry(self.grid_frame, width=200)
                entry.grid(row=row, column=col, padx=10, pady=10)
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Add a submit button to the frame
        self.submit_button = CTk.CTkButton(self, text="Submit", command=lambda: self.submit_verbs())
        self.submit_button.pack(pady=10)

    # Function to handle the submission of data
    def submit_verbs(self):
        # Replace entry boxes with labels
        for row in range(3):
            for col in range(2):
                entry = self.entries[row][col]
                entry_text = self.entries[row][col].get()
                entry.grid_forget()

                if (row == 0 and col== 0):
                    if (entry_text.lower() == self.verb_list.current().yo.lower()):
                        label = CTk.CTkLabel(self.grid_frame, text= entry_text.lower(),
                                             text_color='green')
                        label.grid(row=row, column=col, padx=10, pady=10)
                    else:
                        label = CTk.CTkLabel(self.grid_frame, text= self.verb_list.current().yo.lower(),
                                             text_color = 'red')
                        label.grid(row=row, column=col, padx=10, pady=10)
                elif (row == 0 and col== 1):
                    if (entry_text.lower() == self.verb_list.current().nosotros.lower()):
                        label = CTk.CTkLabel(self.grid_frame, text= entry_text.lower(),
                                             text_color= 'green')
                        label.grid(row=row, column=col, padx=10, pady=10)
                    else:
                        label = CTk.CTkLabel(self.grid_frame, text= self.verb_list.current().nosotros.lower(),
                                             text_color= 'red')
                        label.grid(row=row, column=col, padx=10, pady=10)
                elif (row == 1 and col== 0):
                    if (entry_text.lower() == self.verb_list.current().tu.lower()):
                        label = CTk.CTkLabel(self.grid_frame, text= entry_text.lower(),
                                             text_color= 'green')
                        label.grid(row=row, column=col, padx=10, pady=10)
                    else:
                        label = CTk.CTkLabel(self.grid_frame, text= self.verb_list.current().tu.lower(),
                                             text_color = 'red')
                        label.grid(row=row, column=col, padx=10, pady=10)
                elif (row == 1 and col== 1):
                    if (entry_text.lower() == self.verb_list.current().vosotros.lower()):
                        label = CTk.CTkLabel(self.grid_frame, text= entry_text.lower(),
                                             text_color = 'green')
                        label.grid(row=row, column=col, padx=10, pady=10)
                    else:
                        label = CTk.CTkLabel(self.grid_frame, text= self.verb_list.current().vosotros.lower(),
                                             text_color = 'red')
                        label.grid(row=row, column=col, padx=10, pady=10)
                elif (row == 2 and col== 0):
                    if (entry_text.lower() == self.verb_list.current().el_ella_ud.lower()):
                        label = CTk.CTkLabel(self.grid_frame, text= entry_text.lower(),
                                             text_color = 'green')
                        label.grid(row=row, column=col, padx=10, pady=10)
                    else:
                        label = CTk.CTkLabel(self.grid_frame, text=self.verb_list.current().el_ella_ud.lower(),
                                             text_color = 'red')
                        label.grid(row=row, column=col, padx=10, pady=10)
                elif (row == 2 and col== 1):
                    if (entry_text.lower() == self.verb_list.current().ellos_ellas_uds.lower()):
                        label = CTk.CTkLabel(self.grid_frame, text= entry_text.lower(),
                                             text_color = 'green')
                        label.grid(row=row, column=col, padx=10, pady=10)
                    else:
                        label = CTk.CTkLabel(self.grid_frame, text= self.verb_list.current().ellos_ellas_uds.lower(),
                                             text_color= 'red')
                        label.grid(row=row, column=col, padx=10, pady=10)
                else: 
                    continue
    
        self.submit_button.pack_forget()
        self.submit_button = CTk.CTkButton(self, text="Continue", command=lambda: self.continue_action())
        self.submit_button.pack(pady=10)
        self.verb_list.next()
    
    # Function to handle the continue action
    def continue_action(self):
        self.top_label.configure(text=f"{self.verb_list.current().inf}")
        self.grid_frame.pack_forget()
        self.grid_frame = CTk.CTkFrame(self)
        self.grid_frame.pack(pady=20)

        # Create a new 3x2 grid of entry boxes
        self.entries = []
        for row in range(3):
            row_entries = []
            for col in range(2):
                entry = CTk.CTkEntry(self.grid_frame, width=200)
                entry.grid(row=row, column=col, padx=10, pady=10)
                row_entries.append(entry)
            self.entries.append(row_entries)
        
        self.submit_button.pack_forget()
        self.submit_button = CTk.CTkButton(self, text="Submit", command=lambda: self.submit_verbs())
        self.submit_button.pack(pady=10)

    # Helps incorporate window in the proper place
    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))


# Add term class
class addterm(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        # Opening window for the add term page
        super().__init__(*args, **kwargs)
        self.position_window(300, 250)
        self.title("JakeLingo: Add Term")
        self.resizable(False, False)
        
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

        # Checkbox for Verb
        self.verb_var = CTk.StringVar(value="0")  # Variable to hold the state of the checkbox
        self.checkbox = CTk.CTkCheckBox(self, text="Verb?", variable=self.verb_var, onvalue="1", offvalue="0")
        self.checkbox.grid(row=3, column=0, padx=10, pady=10)

        # Button
        self.button = CTk.CTkButton(self, text="Submit", command= lambda: self.addWord())
        self.button.grid(row=4, column=0, padx=10, pady=20)

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
        app_data_directory = os.path.join(os.path.expanduser('~'), 'spanData')

        os.makedirs(app_data_directory, exist_ok=True)
        filename = 'spanish.csv'
        file_path = os.path.join(app_data_directory, filename)
        df = pd.read_csv(file_path)
        if self.entry.get() in df['Español'].values:
            messagebox.showerror("Error", "Word is already entered.")
            return
        
        # Check if "Verb?" is checked
        is_verb = self.verb_var.get() == "1"
        self.verb_var.set("0")
        
        # The rest is for extracting string from custom tkinter interface
        spwords(span=str(self.entry.get()), classification=str(self.dropdown.get()), verb = is_verb)
        self.entry.delete(0,CTk.END)
        self.dropdown.set('Word Type:')
        self.update_idletasks()
        self.update()

# Final application to incorporate and run all of the code
class Application(CTk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # File setup
        self.setup()

        # Initialize app settings
        CTk.set_appearance_mode('dark')
        CTk.set_default_color_theme("green")
        self.title("JakeLingo")
        self.resizable(False, False)
        self.toplevel_window = None

        # Set the size of the window
        self.position_window(800, 450)

        # Create three frames with borders across the middle
        addButton = CTk.CTkButton(self, text="Add Term", command= lambda:self.open_term())
        addButton.place(x=80, y=390)

        addButton = CTk.CTkButton(self, text="Practice Verbs", command= lambda:self.open_verbs())
        addButton.place(x=330, y=390)

        addButton1 = CTk.CTkButton(self, text="Practice All", command= lambda:self.open_flashcards('all'))
        addButton1.place(x=580, y=390)

       # Conversational frame
        frame1 = CTk.CTkFrame(self, width=200, height=300, fg_color='white')
        frame1.place(x=50, y=50)
        label1 = CTk.CTkLabel(frame1, text="Conversational", text_color='black', font=("Helvetica", 12))
        label1.place(relx=0.5, rely=0.1, anchor='center')
        button1_flashcards = CTk.CTkButton(frame1, text="Flashcards", command= lambda: self.open_flashcards('conversational'))
        button1_flashcards.place(relx=0.5, rely=0.3, anchor='center')
        button1_reading = CTk.CTkButton(frame1, text="Reading", command= lambda: self.open_reading('conversational'))
        button1_reading.place(relx=0.5, rely=0.55, anchor='center')
        button1_writing = CTk.CTkButton(frame1, text="Writing", command= lambda: self.open_writing('conversational'))
        button1_writing.place(relx=0.5, rely=0.8, anchor='center')

        # Scientific frame
        frame2 = CTk.CTkFrame(self, width=200, height=300, fg_color='white')
        frame2.place(x=300, y=50)
        label2 = CTk.CTkLabel(frame2, text="Scientific", text_color='black', font=("Helvetica", 12))
        label2.place(relx=0.5, rely=0.1, anchor='center')
        button2_flashcards = CTk.CTkButton(frame2, text="Flashcards", command= lambda: self.open_flashcards('scientific'))
        button2_flashcards.place(relx=0.5, rely=0.3, anchor='center')
        button2_reading = CTk.CTkButton(frame2, text="Reading", command= lambda: self.open_reading('scientific'))
        button2_reading.place(relx=0.5, rely=0.55, anchor='center')
        button2_writing = CTk.CTkButton(frame2, text="Writing", command= lambda: self.open_writing('scientific'))
        button2_writing.place(relx=0.5, rely=0.8, anchor='center')

        # Advanced frame
        frame3 = CTk.CTkFrame(self, width=200, height=300, fg_color='white')
        frame3.place(x=550, y=50)
        label3 = CTk.CTkLabel(frame3, text="Advanced", text_color='black', font=("Helvetica", 12))
        label3.place(relx=0.5, rely=0.1, anchor='center')
        button3_flashcards = CTk.CTkButton(frame3, text="Flashcards", command= lambda: self.open_flashcards('advanced'))
        button3_flashcards.place(relx=0.5, rely=0.3, anchor='center')
        button3_reading = CTk.CTkButton(frame3, text="Reading", command= lambda: self.open_reading('advanced'))
        button3_reading.place(relx=0.5, rely=0.55, anchor='center')
        button3_writing = CTk.CTkButton(frame3, text="Writing", command= lambda: self.open_writing('advanced'))
        button3_writing.place(relx=0.5, rely=0.8, anchor='center')
    
    # Responsible for setting up the directory if there isn't any
    def setup(self):
        spanDirectory = os.path.join(os.path.expanduser('~'), 'spanData')
        if not os.path.exists(spanDirectory):
            spwords('Español','Classification', 'verb?')
            portfolio('scientific')
            library('scientific')
    
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
                self.toplevel_window = open_flashcards_window('all')  # create window if its None or destroyed

            if button == 'conversational':
                self.toplevel_window = open_flashcards_window('conversational')  # create window if its None or destroyed
            
            if button == 'scientific':
                self.toplevel_window = open_flashcards_window('scientific')  # create window if its None or destroyed
            
            if button == 'advanced':
                self.toplevel_window = open_flashcards_window('advanced')  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
    
     # Opens flashcards specefic to user inquery 
    def open_reading(self, button):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # Opens based on relevant strings coming in to the function
            if button == 'conversational':
                self.toplevel_window = open_reading_window('convo')  # create window if its None or destroyed
            
            if button == 'scientific':
                self.toplevel_window = open_reading_window('science')  # create window if its None or destroyed
            
            if button == 'advanced':
                self.toplevel_window = open_reading_window('advanced')  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
    
    # Opens flashcards specefic to user inquery 
    def open_writing(self, button):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # Opens based on relevant strings coming in to the function

            if button == 'conversational':
                self.toplevel_window = open_writing_window('convo')  # create window if its None or destroyed
            
            if button == 'scientific':
                self.toplevel_window = open_writing_window('science')  # create window if its None or destroyed
            
            if button == 'advanced':
                self.toplevel_window = open_writing_window('advanced')  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
    
    # Responsible for opening the "add term window"
    def open_term(self):
        # Opens window if there isnt one already
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():   
            self.toplevel_window = addterm(self)  # create window if its None or destroyed
            self.toplevel_window.grab_set()
        else:
            self.toplevel_window.focus() 

    def open_verbs(self):
        # Opens verb tense selection window if there isn't one already
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():   
            self.toplevel_window = VerbTenseSelectionWindow(self)  # create window if its None or destroyed
            self.toplevel_window.grab_set()
        else:
            self.toplevel_window.focus()

# Final loop for application
if __name__ == "__main__":
    app = Application()
    app.mainloop()