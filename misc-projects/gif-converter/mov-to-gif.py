import os
import shutil
import ffmpeg
from tkinter import filedialog

# Get directory for movs
vid_input = filedialog.askdirectory(title="Select a Directory")

# Get the path to the desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Define the name of the main folder and subfolders
main_folder_name = input("Enter the folder name: ")
subfolders = ["vid-folder", "out-folder"]

# Create the main folder
main_folder_path = os.path.join(desktop_path, main_folder_name)
os.makedirs(main_folder_path, exist_ok=True)

# Create the subfolders
for subfolder in subfolders:
    subfolder_path = os.path.join(main_folder_path, subfolder)
    os.makedirs(subfolder_path, exist_ok=True)

# Function to convert .mov to .gif
def convert_mov_to_gif(filename):
    if filename.endswith(".mov") or filename.endswith(".mp4"):
        # Construct full file paths
        input_file_path = os.path.join(vid_input, filename)
        # Change the file extension from .mov to .gif
        base_filename = os.path.splitext(filename)[0]
        output_file_path = os.path.join(os.path.join(main_folder_path, 'out-folder'), f"{base_filename}.gif")

        # Use ffmpeg to convert the .mov file to .gif with lower frame rate and resolution
        (
            ffmpeg
            .input(input_file_path)
            .output(output_file_path, vf="fps=8", preset="fast")
            .run()
        )

        print(f"Converted {input_file_path} to {output_file_path}")

        # Move the original .mov file to the vid-folder
        mov_folder_path = os.path.join(main_folder_path, 'vid-folder', filename)
        shutil.move(input_file_path, mov_folder_path)
        print(f"Moved {input_file_path} to {mov_folder_path}")

# List all .mov files in the input directory
mov_files = [f for f in os.listdir(vid_input) if f.endswith(".mov") or f.endswith(".mp4")]

# Convert each .mov file to .gif and move the .mov file to vid-folder
for filename in mov_files:
    convert_mov_to_gif(filename)

# Delete the original mov_input directory
shutil.rmtree(vid_input)
print(f"Deleted the original mov input directory: {vid_input}")


