import tkinter as tk
from tkinter import messagebox
import customtkinter as CTk

class ReadingTopLevel(CTk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.title("Reading Window")
        self.geometry("600x400")
        
        # Set the popup as a modal window
        self.grab_set()
        
        # Create a frame to contain the reading content
        self.content_frame = CTk.CTkFrame(self)
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Example content
        self.content_label = CTk.CTkLabel(self.content_frame, text="This is the reading content.", font=("Arial", 14))
        self.content_label.pack(pady=10, padx=10)
        
        self.content_text = CTk.CTkTextbox(self.content_frame, wrap='word', height=250, width=580)
        self.content_text.insert('1.0', "Reading content goes here...")
        self.content_text.configure(state='disabled')
        self.content_text.pack(pady=10, padx=10)

        # Navigation and Add Term buttons frame
        self.button_frame = CTk.CTkFrame(self)
        self.button_frame.pack(side='bottom', fill='x', pady=10)
        
        # Left button
        self.left_button = CTk.CTkButton(self.button_frame, text="Previous", command=self.navigate_to_previous)
        self.left_button.pack(side='left', padx=10)
        
        # Add Term button
        self.add_term_button = CTk.CTkButton(self.button_frame, text="Add Term", command=self.open_add_term_window)
        self.add_term_button.pack(side='left', padx=10)
        
        # Right button
        self.right_button = CTk.CTkButton(self.button_frame, text="Next", command=self.navigate_to_next)
        self.right_button.pack(side='left', padx=10)
        
    def navigate_to_previous(self):
        # Implement the navigation to the previous entry
        print("Navigate to the previous entry")
        
    def navigate_to_next(self):
        # Implement the navigation to the next entry
        print("Navigate to the next entry")
        
    def open_add_term_window(self):
        # Implement the function to open the Add Term window
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():   
            self.toplevel_window = AddTermWindow(self)  # Create window if it's None or destroyed
            self.toplevel_window.grab_set()
        else:
            self.toplevel_window.focus()  # If window exists, focus it

