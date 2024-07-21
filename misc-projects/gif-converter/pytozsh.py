import os
import shutil
import ffmpeg

# Get directory for mp4s
mp4_input = input("Enter path for mp4 directory: ")

# Get the path to the desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Define the name of the main folder and subfolders
main_folder_name = input("Enter the folder name: ")
subfolders = ["mp4-folder", "out-folder", "Palette"]

# Create the main folder
main_folder_path = os.path.join(desktop_path, main_folder_name)
os.makedirs(main_folder_path, exist_ok=True)

# Create the subfolders
for subfolder in subfolders:
    subfolder_path = os.path.join(main_folder_path, subfolder)
    os.makedirs(subfolder_path, exist_ok=True)

for filename in os.listdir(mp4_input):
    # Check if the file is an mp4
    if filename.endswith(".mp4"):
        # Construct full file paths
        input_file_path = os.path.join(mp4_input, filename)
        output_file_path = os.path.join(os.path.join(main_folder_path, "mp4-folder"), filename)
        # Copy the file
        shutil.copy2(input_file_path, output_file_path)
