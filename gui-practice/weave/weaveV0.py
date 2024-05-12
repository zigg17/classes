import tkinter
import customtkinter as CTk
import os
from PIL import Image
from datetime import datetime

# Initializing app in dark mode
CTk.set_appearance_mode('dark')
app = CTk.CTk()

# Setting up images
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                          "images")
app.logo_image = CTk.CTkImage(Image.open(os.path.join(image_path, "subject.png")), 
                              size=(26, 26))
app.home_image = CTk.CTkImage(light_image=Image.open(os.path.join(image_path, "homeBlack.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "homeWhite.png")), 
                                                 size=(20, 20))
app.meditate_image = CTk.CTkImage(light_image=Image.open(os.path.join(image_path, "meditateBlack.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "meditateWhite.png")), 
                                                 size=(20, 20))
app.journal_image = CTk.CTkImage(light_image=Image.open(os.path.join(image_path, "journalBlack.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "journalWhite.png")), 
                                                 size=(20, 20))
app.bar_image = CTk.CTkImage(light_image=Image.open(os.path.join(image_path, "barBlack.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "barWhite.png")), 
                                                 size=(20, 20))
app.brain_image = CTk.CTkImage(light_image=Image.open(os.path.join(image_path, "brainBlack.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "brainWhite.png")), 
                                                 size=(20, 20))
app.gear_image = CTk.CTkImage(light_image=Image.open(os.path.join(image_path, "gearBlack.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "gearWhite.png")), 
                                                 size=(20, 20))

# Place app in center of the screen
ws = app.winfo_screenwidth() # width of the screen
hs = app.winfo_screenheight() # height of the screen
w = 800 # width for the CTk app
h = 450 # height for the CTk app
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
app.geometry('%dx%d+%d+%d' % (w, h, x, y))

# Title the app
app.title("Weave")

# Placing grid system
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Addition of nav frame
navFrame = CTk.CTkFrame(app,
                        corner_radius = 0)
navFrame.grid(row=0, 
              column=0, 
              sticky="nsew")
navFrame.grid_rowconfigure(6, weight=1)

# Elements in nav frame
navframeLabel = CTk.CTkLabel(navFrame, text="   Weave", 
                             image= app.logo_image, 
                             compound="left", 
                             font= CTk.CTkFont(size=15, weight="bold"))
navframeLabel.grid(row=0, column=0, padx=20, pady=20)

# Home 
def home_button_event():
    select_frame_by_name(app, "home")
home_button = CTk.CTkButton(navFrame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), 
                                                   hover_color=("#c7bccb", "#c7bccb"),
                                                   image=app.home_image, anchor="w", command=home_button_event)
home_button.grid(row=1, column=0, sticky="ew")

# Frame for home
home_frame = CTk.CTkFrame(app, corner_radius=0, fg_color="transparent")
home_frame.grid_columnconfigure(0, weight=1)

# Meditate
def meditate_button_event():
    select_frame_by_name(app, "meditate")

meditate_button = CTk.CTkButton(navFrame, corner_radius=0, height=40, border_spacing=10, text="Meditate",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), 
                                                   hover_color=("#c7bccb", "#c7bccb"),
                                                   image=app.meditate_image, anchor="w", command=meditate_button_event)
meditate_button.grid(row=2, column=0, sticky="ew")

# Frame for meditate
meditate_frame = CTk.CTkFrame(app, corner_radius=0, fg_color="transparent")
meditate_frame.grid_columnconfigure(1, weight=1)
meditate_frame.grid_rowconfigure(1, weight=1)

# meditation timer
def timer_press():
    button_press(app, "timer")

# Varaibles for timer
timer_bool = False
start_time = 0.0
end_time = 0.0
total_time = 0.0

# Establishing a meditation class
class meditatation:
    def __init__(self, date, hours, minutes, seconds, mtype, journal_entry):
        self.date = date
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.type = mtype
        self.type = journal_entry

# Meditation Timer Button
meditate_timer = CTk.CTkButton(meditate_frame, corner_radius=0, height=40, border_spacing=10,
                                text="Begin Meditation", fg_color=("gray70", "gray30"),
                                hover_color = ("#c7bccb", "#c7bccb"), command = timer_press)
meditate_timer.grid(row=4, column=1, padx=20, pady=10)

# Journal
def journal_button_event():
    select_frame_by_name(app, "journal")
journal_button = CTk.CTkButton(navFrame, corner_radius=0, height=40, border_spacing=10, text="Journal",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), 
                                                   hover_color=("#c7bccb", "#c7bccb"),
                                                   image=app.journal_image, anchor="w", command=journal_button_event)
journal_button.grid(row=3, column=0, sticky="ew")

# Frame for journal
journal_frame = CTk.CTkFrame(app, corner_radius=0, fg_color="transparent")

# Stats
def stats_button_event():
    select_frame_by_name(app, "stats")
stats_button = CTk.CTkButton(navFrame, corner_radius=0, height=40, border_spacing=10, text="Stats",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), 
                                                   hover_color=("#c7bccb", "#c7bccb"),
                                                   image=app.bar_image, anchor="w", command=stats_button_event)
stats_button.grid(row=4, column=0, sticky="ew")

# Frame for stats
stats_frame = CTk.CTkFrame(app, corner_radius=0, fg_color="transparent")

# Research
def research_button_event():
    select_frame_by_name(app, "research")
research_button = CTk.CTkButton(navFrame, corner_radius=0, height=40, border_spacing=10, text="Research",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), 
                                                   hover_color=("#c7bccb", "#c7bccb"),
                                                   image=app.brain_image, anchor="w", command=research_button_event)
research_button.grid(row=5, column=0, sticky="ew")

# Frame for resesarch
research_frame = CTk.CTkFrame(app, corner_radius=0, fg_color="transparent")

# Settings
def settings_button_event():
    select_frame_by_name(app, "settings")
settings_button = CTk.CTkButton(navFrame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), 
                                                   hover_color=("#c7bccb", "#c7bccb"),
                                                   image=app.gear_image, anchor="w", command=settings_button_event)
settings_button.grid(row=7, column=0, sticky="ew")

# Frame for settings
settings_frame = CTk.CTkFrame(app, corner_radius=0, fg_color="transparent")

# Selecting through frames
def select_frame_by_name(self, name):
        # set button color for selected button
        home_button.configure(fg_color=("#887191", "#887191") if name == "home" else "transparent")
        meditate_button.configure(fg_color=("#887191", "#887191") if name == "meditate" else "transparent")
        journal_button.configure(fg_color=("#887191", "#887191") if name == "journal" else "transparent")
        stats_button.configure(fg_color=("#887191", "#887191") if name == "stats" else "transparent")
        research_button.configure(fg_color=("#887191", "#887191") if name == "research" else "transparent")
        settings_button.configure(fg_color=("#887191", "#887191") if name == "settings" else "transparent")

        # show selected frame
        if name == "home":
            home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            home_frame.grid_forget()

        if name == "meditate":
            meditate_frame.grid(row=0, column=1, sticky="nsew")
        else:
            meditate_frame.grid_forget()

        if name == "journal":
            journal_frame.grid(row=0, column=1, sticky="nsew")
        else:
            journal_frame.grid_forget()

        if name == "stats":
            stats_frame.grid(row=0, column=1, sticky="nsew")
        else:
            stats_frame.grid_forget()

        if name == "research":
            research_frame.grid(row=0, column=1, sticky="nsew")
        else:
            research_frame.grid_forget()

        if name == "settings":
            settings_frame.grid(row=0, column=1, sticky="nsew")
        else:
            settings_frame.grid_forget()

# For the timer
def button_press(app, name):
    global timer_bool
    global start_time 
    global end_time
    global total_time

    if (not timer_bool):
        meditate_timer.configure(fg_color=("#887191", "#887191") if name == "timer" else ("gray10", "gray90"), 
                                    text = 'End Meditation')
        timer_bool = True
        
        start_time = datetime.now()
    else:
        meditate_timer.configure(fg_color=("gray70", "gray30") if name == "timer" else ("gray10", "gray90"), 
                                    text = 'Begin Meditation')
        
        timer_bool = False
        end_time = datetime.now()
        total_time = end_time - start_time
        print(total_time)

    
# Main loop
app.mainloop()