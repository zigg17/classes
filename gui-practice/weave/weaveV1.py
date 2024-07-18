import tkinter as tk
from tkinter import messagebox
import customtkinter as CTk
from PIL import Image, ImageTk
import datetime
from turtle import RawTurtle, TurtleScreen
import os
import sys
import time
import csv
import re
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns

total = None
date = None
hours = None
minutes = None
seconds = None
mtype = None

class Meditation:
    def __init__(self, date, hours, minutes, seconds, mtype):
        self.date = date
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.mtype = mtype

        app_data_directory = os.path.join(os.path.expanduser('~'), 'weaveData')

        # Create the directory if it doesn't exist
        os.makedirs(app_data_directory, exist_ok=True)

        # Define the filename
        filename = 'meditation_sessions.csv'

        # Define the full file path
        file_path = os.path.join(app_data_directory, filename)

        # Write to the CSV file at the file path
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.date, self.hours, self.minutes, self.seconds, self.mtype])


    @staticmethod
    def load_from_csv(filename):
        meditations = []
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:  # skip empty rows
                        meditations.append(Meditation(*row))
        except FileNotFoundError:
            pass
        return meditations

def sumMeditations():
    app_data_directory = os.path.join(os.path.expanduser('~'), 'weaveData')

    # Create the directory if it doesn't exist
    os.makedirs(app_data_directory, exist_ok=True)

    # Define the filename
    filename = 'meditation_sessions.csv'

    # Define the full file path
    file_path = os.path.join(app_data_directory, filename)
    
    df = pd.read_csv(file_path)

    totalSecs = int(((df.iloc[:,1] * 3600) + (df.iloc[:,2] * 60) + df.iloc[:,3]).sum())
    
    days = totalSecs // (24 * 3600)  # Corrected calculation for days
    hours = (totalSecs % (24 * 3600)) // 3600  # Hours remaining after counting days
    minutes = (totalSecs % 3600) // 60
    seconds = totalSecs % 60

    return [days, hours, minutes, seconds]

class Journal:
    def __init__(self, entry):
        self.entry = entry
        self.entry = self.entry.replace('\n\n', '\n')
        global date

        # Define the directory path for journal data
        app_data_directory = os.path.join(os.path.expanduser('~'), 'weaveData')

        # Create the directory if it doesn't exist
        os.makedirs(app_data_directory, exist_ok=True)

        # Define the filename (you can also use dates or other identifiers for unique filenames)
        filename = 'journal.txt'

        # Define the full file path
        file_path = os.path.join(app_data_directory, filename)
        
        american_datetime = date.strftime("%m/%d/%Y %I:%M:%S %p")
        # Write the journal entry to the file
        with open(file_path, mode='a') as file:
            file.write( american_datetime + "\n"+ self.entry + "\n\n")

def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

def parse_journal_entries_from_file():
    # Define the directory and file paths
    app_data_directory = os.path.join(os.path.expanduser('~'), 'weaveData')
    filename = 'journal.txt'
    file_path = os.path.join(app_data_directory, filename)

    # Ensure the directory exists
    os.makedirs(app_data_directory, exist_ok=True)

    # Check if the file exists before trying to read
    if not os.path.exists(file_path):
        print("The file does not exist.")
        return []

    with open(file_path, 'r') as file:
        text = file.read()

    # Regex pattern to match date-time stamps
    pattern = r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} [AP]M)'

    # Split the text based on the date-time pattern
    entries = re.split(pattern, text)

    # Iterate through the entries and extract date-time stamps and bodies
    parsed_entries = []
    for i in range(1, len(entries), 2):
        date_time = entries[i].strip()
        # Retain the formatting (including tabs) of the body
        body = entries[i + 1].lstrip('\n')
        parsed_entries.append({'date': date_time, 'body': body})

    return parsed_entries


def process_journal_file():
    # Define the directory path for journal data
    app_data_directory = os.path.join(os.path.expanduser('~'), 'weaveData')

    # Create the directory if it doesn't exist
    os.makedirs(app_data_directory, exist_ok=True)

    # Define the filename
    filename = 'journal.txt'

    # Define the full file path
    file_path = os.path.join(app_data_directory, filename)

    # Read the text from the file
    with open(file_path, 'r') as file:
        input_text = file.read()

    # Regular expression pattern for date-time with optional leading tabs
    pattern = r'(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} [AP]M)'

    # Split the text based on the date-time pattern
    entries = re.split(pattern, input_text)

    # Reconstruct the text with controlled line breaks and preserve leading tabs
    processed_text = ''
    for i in range(1, len(entries), 2):  # Iterate through matched date-time and corresponding entries
        date_time = entries[i].strip()
        entry = entries[i + 1].lstrip('\n').rstrip()
        processed_text += "\n" + date_time + "\n" + entry + "\n\n"
    
    # Write the processed text back to the file
    with open(file_path, 'w') as file:
        file.write(processed_text)


class Application(CTk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize app settings
        CTk.set_appearance_mode('dark')
        self.title("Weave")
        self.setup_images()
        self.position_window(800, 450)
        self.resizable(False, False)
        self.iconpath = ImageTk.PhotoImage(file=resource_path(os.path.join("images", "subject.ico")))

        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)

        self.directory_path = os.path.join(os.path.expanduser('~'), 'weaveData','userData.txt')
        self.user = self.username()
        

        # Create frames
        self.navFrame = NavigationFrame(self)
        self.navFrame.grid(row=0, column=0, sticky="nsew")
        self.homeFrame = HomeFrame(self)
        self.navFrame.home_button.configure(fg_color=("#887191", "#887191"))
        self.homeFrame.grid(row=0, column=1, sticky="nsew") 
        self.journalFrame = JournalFrame(self)
        self.meditationFrame = MeditationFrame(self)
        self.statsFrame = StatsFrame(self)
        self.settingsFrame = SettingsFrame(self)
        self.homeFrame.start_turtle_drawing()
        # Other frames can be initialized here...

    def username(self):
        if os.path.exists(self.directory_path):
            with open(self.directory_path, 'r') as file:
                # Read the first line
                name = file.readline()
                
                if name == "":
                    name = self.getUsername()
                    with open(self.directory_path, 'w') as file:
                        file.write(name)
                return name
        else:
            Meditation('Date','Hours','Minutes','Seconds','Meditation')
            name = self.getUsername()
            with open(self.directory_path, 'w') as file:
                file.write(name)
            return name
            
    
    def submit_username(self, window, entry):
        entered_username = entry.get()
        if len(entered_username) > 14 or len(entered_username) == 0:
            messagebox.showerror(title = "Error",
                                 message = "Name must be 14 characters or shorter and cannot contain no characters.")

            entry.delete(0, CTk.END)  # Clear the entry field for new input
        else:
            self.username = entered_username
            window.destroy()

    def getUsername(self):
        # Create a new window
        input_window = CTk.CTkToplevel(self)
        input_window.title("Enter Username")
        input_window.geometry("{}x{}+{}+{}".format(300,125,self.winfo_rootx()+700, self.winfo_rooty()+375))
        
        # CTkEntry for input
        username_entry = CTk.CTkEntry(input_window, placeholder_text="Enter username")
        username_entry.pack(pady=20)
        
        # Submit button
        submit_button = CTk.CTkButton(input_window, text="Submit", 
                                      command=lambda: self.submit_username(input_window, username_entry)
                                      ,fg_color=("gray70", "gray30"), hover_color= ("#c7bccb", "#c7bccb"))
        submit_button.pack()

        # Wait for the window to close
        self.wait_window(input_window)

        return self.username
        

    def select_frame_by_name(self, name):
        # Update button colors in navFrame
        self.navFrame.update_button_color(name)

        # Grid management for frames
        if name == "home":
            self.homeFrame.grid(row=0, column=1, sticky="nsew")
        else:
            self.homeFrame.grid_forget()

        if name == "meditation":
            self.meditationFrame.grid(row=0, column=1, sticky="nsew")
        else:
            self.meditationFrame.grid_forget()

        if name == "journal":
            self.journalFrame.grid(row=0, column=1, sticky="nsew")
        else:
            self.journalFrame.grid_forget()
        
        if name == "stats":
            self.statsFrame.grid(row=0, column=1, sticky="nsew")
        else:
            self.statsFrame.grid_forget()
        
        if name == "settings":
            self.settingsFrame.grid(row=0, column=1, sticky="nsew")
        else:
            self.settingsFrame.grid_forget()

    
    def setup_images(self):
        self.logo_image = CTk.CTkImage(Image.open(resource_path(os.path.join("images", "subject.png"))), 
                                       size=(26, 26))
        self.home_image = CTk.CTkImage(light_image=Image.open(resource_path(os.path.join("images", "homeBlack.png"))),
                                    dark_image=Image.open(resource_path(os.path.join("images", "homeWhite.png"))), 
                                    size=(20, 20))
        self.meditate_image = CTk.CTkImage(light_image=Image.open(resource_path(os.path.join("images", "meditateBlack.png"))),
                                        dark_image=Image.open(resource_path(os.path.join("images", "meditateWhite.png"))), 
                                        size=(20, 20))
        self.journal_image = CTk.CTkImage(light_image=Image.open(resource_path(os.path.join("images", "journalBlack.png"))),
                                        dark_image=Image.open(resource_path(os.path.join("images", "journalWhite.png"))), 
                                        size=(20, 20))
        self.bar_image = CTk.CTkImage(light_image=Image.open(resource_path(os.path.join("images", "barBlack.png"))),
                                    dark_image=Image.open(resource_path(os.path.join("images", "barWhite.png"))), 
                                    size=(20, 20))
        self.brain_image = CTk.CTkImage(light_image=Image.open(resource_path(os.path.join("images", "brainBlack.png"))),
                                        dark_image=Image.open(resource_path(os.path.join("images", "brainWhite.png"))), 
                                        size=(20, 20))
        self.gear_image = CTk.CTkImage(light_image=Image.open(resource_path(os.path.join("images", "gearBlack.png"))),
                                    dark_image=Image.open(resource_path(os.path.join("images", "gearWhite.png"))), 
                                    size=(20, 20))
        self.left_image = CTk.CTkImage(light_image=Image.open(resource_path(os.path.join("images", "leftBlack.png"))),
                                    dark_image=Image.open(resource_path(os.path.join("images", "leftWhite.png"))), 
                                    size=(20, 20))
        self.right_image = CTk.CTkImage(light_image=Image.open(resource_path(os.path.join("images", "rightBlack.png"))),
                                        dark_image=Image.open(resource_path(os.path.join("images", "rightWhite.png"))), 
                                        size=(20, 20))


    def position_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

class NavigationFrame(CTk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0)
        self.parent = parent
        self.grid_rowconfigure(9, weight=1)
        self.create_widgets()
    
    def update_button_color(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("#887191", "#887191") if name == "home" else "transparent")
        self.meditation_button.configure(fg_color=("#887191", "#887191") if name == "meditation" else "transparent")
        self.journal_button.configure(fg_color=("#887191", "#887191") if name == "journal" else "transparent")
        self.stats_button.configure(fg_color=("#887191", "#887191") if name == "stats" else "transparent")
        self.research_button.configure(fg_color=("#887191", "#887191") if name == "research" else "transparent")
        self.settings_button.configure(fg_color=("#887191", "#887191") if name == "settings" else "transparent")

    def create_widgets(self):
        self.navframeLabel = CTk.CTkLabel(self, text="   Weave", 
                                          image=self.parent.logo_image, 
                                          compound="left", 
                                          font=CTk.CTkFont(size=15, weight="bold"))
        self.navframeLabel.grid(row=0, column=0, padx=20, pady=20)
        
        self.home_button = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Home",
                                         fg_color="transparent", text_color=("gray10", "gray90"), 
                                         hover_color=("#c7bccb", "#c7bccb"),
                                         image=self.parent.home_image, anchor="w", command = self.on_home_click)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.meditation_button = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Meditate",
                                         fg_color="transparent", text_color=("gray10", "gray90"), 
                                         hover_color=("#c7bccb", "#c7bccb"),
                                         image=self.parent.meditate_image, anchor="w", command = self.on_meditation_click)
        self.meditation_button.grid(row=2, column=0, sticky="ew")

        self.journal_button = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Journal",
                                         fg_color="transparent", text_color=("gray10", "gray90"), 
                                         hover_color=("#c7bccb", "#c7bccb"),
                                         image=self.parent.journal_image, anchor="w", command = self.on_journal_click)
        self.journal_button.grid(row=3, column=0, sticky="ew")

        self.stats_button = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Stats",
                                         fg_color="transparent", text_color=("gray10", "gray90"), 
                                         hover_color=("#c7bccb", "#c7bccb"),
                                         image=self.parent.bar_image, anchor="w", command = self.on_stats_click)
        self.stats_button.grid(row=4, column=0, sticky="ew")

        self.research_button = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Research",
                                         fg_color="transparent", text_color=("gray10", "gray90"), 
                                         hover_color=("#c7bccb", "#c7bccb"),
                                         image=self.parent.brain_image, anchor="w", command = self.on_research_click)
        self.research_button.grid(row=5, column=0, sticky="ew")

        self.boof_button = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="",
                                         fg_color="transparent",hover_color= ("#2b2b2b", "#2b2b2b"),
                                           text_color=("gray10", "gray90"), anchor="w")
        self.boof_button.grid(row=6, column=0, sticky="ew")

        self.boof_button = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="",
                                         fg_color="transparent",hover_color= ("#2b2b2b", "#2b2b2b"),
                                           text_color=("gray10", "gray90"), anchor="w")
        self.boof_button.grid(row=6, column=0, sticky="ew")
        
        self.boof_button = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="",
                                         fg_color="transparent",hover_color= ("#2b2b2b", "#2b2b2b"),
                                           text_color=("gray10", "gray90"), anchor="w")
        self.boof_button.grid(row=7, column=0, sticky="ew")

        self.boof_button = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="",
                                         fg_color="transparent",hover_color= ("#2b2b2b", "#2b2b2b"),
                                           text_color=("gray10", "gray90"), anchor="w")
        self.boof_button.grid(row=8, column=0, sticky="ew")

        self.settings_button = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                         fg_color="transparent", text_color=("gray10", "gray90"), 
                                         hover_color=("#c7bccb", "#c7bccb"),
                                         image=self.parent.gear_image, anchor="w", command = self.on_settings_click)
        self.settings_button.grid(row=9, column=0, sticky="ew")
    
    def on_home_click(self):
        self.parent.select_frame_by_name("home")
        self.parent.homeFrame.start_turtle_drawing()
    
    def on_meditation_click(self):
        self.parent.select_frame_by_name("meditation")
    
    def on_journal_click(self):
        self.parent.select_frame_by_name("journal")

    def on_stats_click(self):
        self.parent.select_frame_by_name("stats")
    
    def on_research_click(self):
        self.parent.select_frame_by_name("research")

    def on_settings_click(self):
        self.parent.select_frame_by_name("settings")

class HomeFrame(CTk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.parent = parent

        # Set the size of the SettingsFrame
        self.width = 660  # Adjust the width as needed
        self.height = 200  # Adjust the height as needed
        self.configure(width=self.width, height=self.height)
        
        self.turtle_canvas = tk.Canvas(self, width=600, height=670, highlightthickness=0)  # Adjust size as needed
        self.turtle_canvas.place(x = 28, y = -10) # Adjust position as needed
        self.turtle_screen = TurtleScreen(self.turtle_canvas)
        self.turtle_screen.bgcolor('#242424')
        self.turtle = RawTurtle(self.turtle_screen)
        self.turtle.hideturtle()  # Hide turtle until drawing starts
        self.turtle_screen.tracer(0, 0)  # Disable automatic updates for performanc

        # Create a frame to overlay on the canvas
        self.overlay_frame = CTk.CTkFrame(self.turtle_canvas, width=100, height=50, corner_radius=10,
                                          fg_color=("gray70", "gray30"))
        self.overlay_frame.place(relx=0.5, rely=0.35, anchor='center')

        
        
        # Create a new frame for the switch with specified width and height
        self.title_frame = CTk.CTkFrame(self.turtle_canvas, fg_color='transparent', 
                                         width= 100, height=50)

        # Place switch_frame at the bottom right corner
        self.title_frame.place(x= 10, y= 420)

        # Place label and switch inside the switch_frame
        self.mode_label = CTk.CTkLabel(self.title_frame, text=f"Welcome, {self.parent.user}.", 
                                       font = ("", 17, 'bold'))
        self.mode_label.pack(side='left', padx=5, pady=5)

        # Create a new frame for the switch with specified width and height
        self.date_frame = CTk.CTkFrame(self.turtle_canvas, fg_color='transparent', 
                                         width= 100, height=50)

        self.date_frame.place(x= 485, y= 10)
        # Place label and switch inside the switch_frame
        self.mode_label = CTk.CTkLabel(self.date_frame, text=f"{datetime.datetime.now().date()}", 
                                       font = ("", 17, 'bold'))
        self.mode_label.pack(side='left', padx=5, pady=5)
        
        self.total = sumMeditations()
        # Example content inside the frame
        self.label = CTk.CTkLabel(self.overlay_frame,
                                  text=f"{self.total[0]}d {self.total[1]}h {self.total[2]}m {self.total[3]}s")
        self.label.pack(pady=10, padx=10)
    
    def relabel(self):
        self.total = sumMeditations()
        # Example content inside the frame
        self.label.configure(text = f"{self.total[0]}d {self.total[1]}h {self.total[2]}m {self.total[3]}s")

    def start_turtle_drawing(self):
        colors = ['#6a50a4', '#482980', 'purple', '#482980', '#6a50a4', 'purple']
        self.turtle.clear()  # Clear existing drawings if any
        self.turtle.penup()
        self.turtle.home()
        self.turtle.pendown()
    
        for i in range(200):
            self.turtle.pencolor(colors[i % 6])
            self.turtle.circle(100, 60-i)
            self.turtle.left(i)
            self.turtle_screen.update()
            time.sleep(.01)
        
        self.turtle.penup()
        self.turtle.hideturtle() 



class MeditationFrame(CTk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.parent = parent
        self.grid_columnconfigure(1, weight=1) # Adjust weights as necessary
        self.grid_rowconfigure(1, weight=1)

        # Global variables for saving
        global date
        global hours
        global minutes
        global seconds
        global mtype
        global total

        # Initialize variables for the timer
        self.timer_bool = False
        self.start_time = 0.0
        self.end_time = 0.0
        self.total_time = 0.0

        self.turtle_canvas = tk.Canvas(self, width=500, height=300)  # Adjust size as needed
        self.turtle_canvas.grid(row=1, column=1, columnspan=3)  # Adjust position as needed
        self.turtle_screen = TurtleScreen(self.turtle_canvas)
        self.turtle_screen.bgcolor('black')
        self.turtle = RawTurtle(self.turtle_screen)
        self.turtle.hideturtle()  # Hide turtle until drawing starts
        self.turtle_screen.tracer(0, 0)  # Disable automatic updates for performanc

        # Create a label for messages, initially hidden
        self.message_label = CTk.CTkLabel(self, text="", text_color= 'red')
        self.message_label.grid(row=3, column=1, columnspan=3)
        self.message_label.grid_remove()  # Hide the label initially

        # Create and place the meditation timer button
        self.meditate_timer = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                            text="Begin Meditation", fg_color=("gray70", "gray30"),
                                            hover_color=("#c7bccb", "#c7bccb"), command=self.on_timer_press)
        self.meditate_timer.grid(row=4, column=1, padx=40, pady=20)

        meditation_types = ['Concentration', 'Breathwork', 'Mindfulness']

        # Create and place the dropdown list
        self.meditation_dropdown = CTk.CTkComboBox(self, values=meditation_types, state='readonly', )
        self.meditation_dropdown.grid(row=4, column=2, padx=40, pady=20)
        self.meditation_dropdown.set('Select Style:')

        journal_sesh = ['Yes', 'No']

        # Create and place the dropdown list
        self.journal_dropdown = CTk.CTkComboBox(self, values = journal_sesh, state='readonly')
        self.journal_dropdown.grid(row=4, column=3, padx=40, pady=20)
        self.journal_dropdown.set('Journal:')

    def show_temporary_message(self, message):
        self.message_label.configure(text=message)
        self.message_label.grid()  # Show the label
        self.after(3000, self.message_label.grid_remove)  # Hide after 3000 milliseconds

    def create_journal_popup(self):
        # Create a new top-level window
        self.journal_window = tk.Toplevel(self)
        self.journal_window.title("Journal Entry")

        # Position the new window relative to the main window
        self.journal_window.geometry("+{}+{}".format(self.winfo_rootx()+100, self.winfo_rooty()+75))

        # Create a text entry box
        self.journal_entry = CTk.CTkTextbox(self.journal_window, height=300, width=500, wrap = 'word')
        self.journal_entry.pack(padx=10, pady=10)

        # Create a submit button
        submit_button = CTk.CTkButton(self.journal_window, text="Submit", command=self.submit_journal_entry)
        submit_button.pack(pady=10)

            
    def submit_journal_entry(self):
        # Get text from the text entry box
        journal_text = self.journal_entry.get("1.0", "end-1c")

        # Ask for confirmation
        if messagebox.askyesno("Confirm", "Are you sure you want to submit?"):
            # Process the journal text as needed
            Journal(journal_text)

            self.parent.journalFrame.load_most_recent_entry()
            self.parent.journalFrame.initialize_journal_entries()
            # Close the journal popup window
            self.journal_window.destroy()
        else:
            # User decided not to submit, you can handle it here
            pass  # Do nothing, or perhaps provide feedback to the user


    def on_timer_press(self):
        global date
        if self.meditation_dropdown.get() == 'Select Style:' or self.journal_dropdown.get() == 'Journal':
            # Handle the case where selections are not made
            self.show_temporary_message("Please make selections in both ComboBoxes before starting.")
            return  # Exit the method

        if not self.timer_bool:
            self.meditate_timer.configure(fg_color=("#887191", "#887191"), text='End Meditation')
            self.timer_bool = True
            self.start_time = datetime.datetime.now()
            self.start_turtle_drawing()
        else:
            self.meditate_timer.configure(fg_color=("gray70", "gray30"), text='Begin Meditation')
            self.timer_bool = False
            self.end_time = datetime.datetime.now()
            self.total_time = self.end_time - self.start_time

            # Handle meditation completion (e.g., logging meditation session)
            total = str(self.total_time)[:-4]
            date = datetime.datetime.now()
            seconds = float(total.split(":")[2])
            minutes = float(total.split(":")[1])
            hours = float(total.split(":")[0])
            mtype = self.meditation_dropdown.get()
            Meditation(date, hours, minutes, seconds, mtype)
            self.parent.homeFrame.relabel()
            self.parent.statsFrame.update_plots()

            if self.journal_dropdown.get() == 'Yes':
                self.create_journal_popup()
                

    
    def start_turtle_drawing(self):
        colors = ['#6a50a4', '#482980', '#6a50a4', '#482980', '#6a50a4', '#482980']
        self.turtle.clear()  # Clear existing drawings if any
        self.turtle.home() 
       # Set the drawing speed (1 is slowest, 10 is fast, 0 is no animation)
        self.turtle.speed(1)
        while(True):
            for x in range(360):
                self.turtle.pencolor(colors[x % 6])
                self.turtle.width(x // 100 + 1)
                self.turtle.forward(x)
                self.turtle.left(59)
                self.turtle_screen.update()  # Update the screen after each step
                time.sleep(.05)
                if(not self.timer_bool):
                    break
            self.turtle.home() 
            self.turtle.clear()

            if(not self.timer_bool):
                break


class JournalFrame(CTk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.parent = parent
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)


        self.journal_frame = CTk.CTkFrame(self,width = 600, height= 250)
        self.journal_frame.grid(row=1, column=1, columnspan=4)
        self.load_most_recent_entry()

        self.sorted_entries = []
        self.current_entry_index = None
        self.initialize_journal_entries()

        self.left_button = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                         image=self.parent.left_image, text="", fg_color=("gray70", "gray30"),
                                         hover_color=("#c7bccb", "#c7bccb"))
        self.left_button.grid(row=4, column=1, padx=40, pady=20)

        # Replace right_button with right arrow button
        self.right_button = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                         image=self.parent.right_image, text="", fg_color=("gray70", "gray30"),
                                         hover_color=("#c7bccb", "#c7bccb"))
        self.right_button.grid(row=4, column=2, padx=40, pady=20)
        self.left_button.configure(command=self.navigate_to_previous_entry)
        self.right_button.configure(command=self.navigate_to_next_entry)

        # Create and place the dropdown list
        self.journal_search = CTk.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                             text="Search By Date", fg_color=("gray70", "gray30"),
                                         hover_color=("#c7bccb", "#c7bccb"), command= self.open_journal_entries_popup)
        self.journal_search.grid(row=4, column=3, padx=40, pady=20)

    def initialize_journal_entries(self):
        journal_entries = parse_journal_entries_from_file()
        self.sorted_entries = sorted(journal_entries, 
                                     key=lambda e: datetime.datetime.strptime(e['date'],"%m/%d/%Y %I:%M:%S %p"), reverse=True)
        if self.sorted_entries:
            self.current_entry_index = 0
            self.on_journal_entry_click(self.sorted_entries[0])

    def navigate_to_previous_entry(self):
        if self.sorted_entries and self.current_entry_index > 0:
            self.current_entry_index -= 1
            self.on_journal_entry_click(self.sorted_entries[self.current_entry_index])

    def navigate_to_next_entry(self):
        if self.sorted_entries and self.current_entry_index < len(self.sorted_entries) - 1:
            self.current_entry_index += 1
            self.on_journal_entry_click(self.sorted_entries[self.current_entry_index])

    def load_most_recent_entry(self):
        # Parse journal entries from file
        journal_entries = parse_journal_entries_from_file()

        # Find the most recent entry
        if journal_entries:
            most_recent_entry = max(journal_entries,
                                    key=lambda e: datetime.datetime.strptime(e['date'], "%m/%d/%Y %I:%M:%S %p"))
            self.on_journal_entry_click(most_recent_entry)
    
    def open_journal_entries_popup(self):
        # Create a new top-level window for journal entries
        self.journal_search.configure(hover_color=("gray70", "gray30"))
        self.journal_entries_window = tk.Toplevel(self)
        self.journal_entries_window.geometry("+{}+{}".format(self.winfo_rootx()+100, self.winfo_rooty()+75))
        self.journal_entries_window.title("Journal Entries")

        # Set the popup as a modal window
        self.journal_entries_window.grab_set()

        # Use a scrollable frame to accommodate a large number of entries
        scrollable_frame = CTk.CTkScrollableFrame(self.journal_entries_window)
        scrollable_frame.pack(fill='both', expand=True)

        # Parse journal entries from file
        journal_entries = parse_journal_entries_from_file()

        # Sort the entries in reverse chronological order
        sorted_entries = sorted(journal_entries,
                                key=lambda e: datetime.datetime.strptime(e['date'], "%m/%d/%Y %I:%M:%S %p"), reverse=True)

        # Create a button for each journal entry
        for entry in sorted_entries:
            date_button = CTk.CTkButton(scrollable_frame, text=entry['date'],
                                        command=lambda e=entry: self.process_and_close_popup(e),
                                        fg_color=("#887191", "#887191"), hover_color= ("#c7bccb", "#c7bccb"))
            date_button.pack(pady=5, padx=10, fill='x')

    def process_and_close_popup(self, entry):
        # Process the entry (e.g., update journal frame)
        self.on_journal_entry_click(entry)
        self.journal_search.configure(hover_color=("#c7bccb", "#c7bccb"))

        # Close the popup window
        self.journal_entries_window.destroy()

    def on_journal_entry_click(self, entry):
        # Clear the current contents of the journal_frame
        for widget in self.journal_frame.winfo_children():
            widget.destroy()

        # Display the date of the entry
        date_label = CTk.CTkLabel(self.journal_frame, text=f"Date: {entry['date']}", font=("Arial", 14))
        date_label.pack(pady=10, padx=10)

        # Display the content of the journal entry in a read-only text widget
        content_text = CTk.CTkTextbox(self.journal_frame, wrap='word', height=250, width=600)
        content_text.insert('1.0', entry['body'])
        content_text.configure(state='disabled')
        content_text.pack(pady=10, padx=10)

class StatsFrame(CTk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.parent = parent
        # Set the size of the SettingsFrame
        self.width = 630  # Adjust the width as needed
        self.height = 200  # Adjust the height as needed
        self.configure(width=self.width, height=self.height)

        # Load meditation data
        self.meditation_data = self.load_meditation_data()

        # Process data for plotting
        self.process_data()

        # Set up the figures for each plot
        self.figures = [Figure(figsize=(3, 3), dpi=100) for _ in range(4)]
        self.create_plots()

        # Create canvas for each figure and add to the frame
        for i, fig in enumerate(self.figures):
            canvas = FigureCanvasTkAgg(fig, master=self)
            widget = canvas.get_tk_widget()
            widget.grid(row=i, column=0, padx=10, pady=10, sticky="nsew")  # One plot per row
            canvas.draw()

    def update_plots(self):
        # Clear the old figures
        for fig in self.figures:
            fig.clf()

        # Reload and process the meditation data
        self.meditation_data = self.load_meditation_data()
        self.process_data()

        # Recreate the plots
        self.create_plots()

    def load_meditation_data(self):
        app_data_directory = os.path.join(os.path.expanduser('~'), 'weaveData')
        filename = 'meditation_sessions.csv'
        file_path = os.path.join(app_data_directory, filename)
        try:
            df = pd.read_csv(file_path)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except FileNotFoundError:
            print("File not found. Ensure the meditation_sessions.csv file exists.")
            return pd.DataFrame()

    def process_data(self):
        if not self.meditation_data.empty:
            # Calculate total time in minutes
            self.meditation_data['TotalTime'] = self.meditation_data['Hours'] * 60 + \
                self.meditation_data['Minutes'] + self.meditation_data['Seconds'] / 60
            self.meditation_data['Weekday'] = self.meditation_data['Date'].dt.day_name()

    def create_plots(self):

        # Define a function to update the colors of plot elements
        def update_plot_colors(ax):
            ax.tick_params(colors=text_color, which='both')  # Tick colors
            ax.figure.patch.set_edgecolor('white') 
            ax.figure.patch.set_linewidth(1)  # Border width
            for spine in ax.spines.values():  # Spine colors
                spine.set_edgecolor(text_color)
            ax.yaxis.label.set_color(text_color)  # Y label color
            ax.xaxis.label.set_color(text_color)  # X label color
            ax.title.set_color(text_color)  # Title color
            ax.title.set_color(text_color)
        
        if not self.meditation_data.empty:
            sns.set(rc={'axes.facecolor':'#4d4d4d'})
            text_color = 'white'  # Set text color
            # Define a purple color palette  # Or define your own shades of purple

            # Set the Seaborn palette to the purple palette
            
            fig_width, fig_height = 6, 5  # Adjust these dimensions as needed
            # Plot 1: Meditations by Meditation Type
            self.figures[0].set_size_inches(fig_width, fig_height)
            self.figures[0].set_facecolor('#242424')
            ax0 = self.figures[0].add_subplot(111)
            sns.countplot(data=self.meditation_data, x='Meditation', ax=ax0, palette='Purples')
            self.figures[0].suptitle('Meditations by Meditation Type', color = 'white')
            update_plot_colors(ax0)

            # Plot 2: Average Meditation Time per Weekday
            self.figures[1].set_size_inches(fig_width, fig_height)
            self.figures[1].set_facecolor('#242424')
            ax1 = self.figures[1].add_subplot(111)
            weekday_avg = self.meditation_data.groupby('Weekday')['TotalTime'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
            sns.barplot(x=weekday_avg.index, y=weekday_avg.values, ax=ax1, palette='Purples')
            self.figures[1].suptitle('Average Meditation Time per Weekday',color = 'white')
            ax1.set_xticklabels(['M', 'T', 'W', 'R', 'F', 'S', 'U'])
            update_plot_colors(ax1)

            # Plot 3: Average Meditation Time per Meditation Type
            self.figures[2].set_size_inches(fig_width, fig_height)
            self.figures[2].set_facecolor('#242424')
            ax2 = self.figures[2].add_subplot(111)
            type_avg = self.meditation_data.groupby('Meditation')['TotalTime'].mean()
            sns.barplot(x=type_avg.index, y=type_avg.values, ax=ax2, palette='Purples')
            self.figures[2].suptitle('Average Meditation Time per Meditation Type', color = 'white')
            update_plot_colors(ax2)

            # Plot 4: Meditation Time Over Day
            self.figures[3].set_size_inches(fig_width, fig_height)
            self.figures[3].set_facecolor('#242424')
            ax3 = self.figures[3].add_subplot(111)
            self.meditation_data['Hour'] = self.meditation_data['Date'].dt.hour
            hourly_sum = self.meditation_data.groupby('Hour')['TotalTime'].sum()
            sns.lineplot(x=hourly_sum.index, y=hourly_sum.values, ax=ax3, palette='Purples')
            self.figures[3].suptitle('Meditation Time Over Day', color = 'white')
            update_plot_colors(ax3)
        else:
            print("No data available for plotting.")



class SettingsFrame(CTk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.parent = parent

        # Set the size of the SettingsFrame
        self.width = 660  # Adjust the width as needed
        self.height = 200  # Adjust the height as needed
        self.configure(width=self.width, height=self.height)


# Running the application
if __name__ == "__main__":
    app = Application()
    app.mainloop()
    process_journal_file()
    entries = parse_journal_entries_from_file()