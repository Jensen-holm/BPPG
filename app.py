import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
import os

import pandas as pd

ctk.set_appearance_mode("system")

root = ctk.CTk()
root.geometry("800x600")
root.title("Backprop Playground")
root.minsize(600, 400)


# global variables set by buttons
# here we are defining defaults
global ARGS
ARGS = {
    "data": None,  # will be a pandas dataframe
    "test_size": 0.2,  # will always be positive float
    "hidden_size": 8,  # will always be EVEN integer
    "epochs": 1000,  # will always be positive integer
    "target": "",  # will be a string
    "features": [],  # will be a list of strings
}


upload = Image.open("assets/upload.png")
upload_img = ctk.CTkImage(
    light_image=upload,
    dark_image=upload,
)


def upload_file():
    global data
    # eventually we will want to save datasets
    # into the application and be able to select
    # previous datasets as well
    file = ctk.filedialog.askopenfile()
    try:
        df = pd.read_csv(file)
        ARGS["data"] = file
        # save the dataset as a csv for later use
        save_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(save_dir, exist_ok=True)  # ensure 'data' folder exists
        save_path = os.path.join(save_dir, os.path.basename(file.name))
        df.to_csv(save_path)

        # once data is successfully uploaded,
        # we want to open up a new screen with
        # options for training the neural network
        open_training_window()
    except Exception as e:
        messagebox.showerror(
            title="CSV Error",
            message=f"{e}",
        )


upload_csv_button = ctk.CTkButton(
    text="Upload CSV",
    image=upload_img,
    master=root,
    command=upload_file,
    font=("Consolas", 16),
)

upload_csv_button.place(
    relx=0.5,
    rely=0.5,
    anchor=tk.CENTER,
)


# for when the user successfully uploads or selects
# a valid csv dataset for their neural network
def open_training_window():
    # Clear the current widgets in the root window
    for widget in root.winfo_children():
        widget.destroy()

    # add grid for hyper tuning neural network parameters


if __name__ == "__main__":
    root.mainloop()
