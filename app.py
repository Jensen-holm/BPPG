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

# csv upload pane
# Create a frame for the left pane
left_frame = tk.Frame(root)
left_frame.grid(row=0, column=0, sticky="nsew")

# Create a frame for the right pane
right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, sticky="nsew")

# place logo in center
# right now this picture is too small
logo = Image.open(os.path.join(os.getcwd(), "assets/backprop_playground.png"))
logo_img = ctk.CTkImage(
    light_image=logo,
    dark_image=logo,
)
logo_label = ctk.CTkLabel(
    master=root,
    image=logo_img,
    text="",
)
logo_label.place(
    relx=0.5,
    rely=0.5,
    anchor=tk.CENTER,
)


def is_csv_file(file_path):
    # Check if the file extension is ".csv"
    file_extension = os.path.splitext(file_path)[-1]
    return file_extension.lower() == ".csv"


def csv_files():
    data_path = os.path.join(os.getcwd(), "data")
    csvs = []
    for f in os.listdir(data_path):
        if is_csv_file(f):
            csvs.append(f)
    return csvs


def upload_file():
    global data
    # eventually we will want to save datasets
    # into the application and be able to select
    # previous datasets as well
    file = ctk.filedialog.askopenfile()
    try:
        if not file:
            # if user didnt upload anything
            # I don't want to show error
            return

        if not is_csv_file(file.name):
            ext = os.path.splitext(file)[-1]
            messagebox.showerror(
                title="Invalid file type",
                message=f"please upload a CSV file. not a '{ext}'",
            )

        df = pd.read_csv(file)
        ARGS["data"] = file
        # save the dataset as a csv for later use
        save_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(save_dir, exist_ok=True)  # ensure 'data' folder exists
        save_path = os.path.join(save_dir, os.path.basename(file.name))
        df.to_csv(save_path)

        # open training window once the data is uploaded
        open_training_window()
    except Exception as e:
        messagebox.showerror(
            title="CSV Error",
            message=f"{e}",
        )
        raise e


upload = Image.open(os.path.join(os.getcwd(), "assets/upload.png"))
upload_img = ctk.CTkImage(
    light_image=upload,
    dark_image=upload,
)

upload_csv_button = ctk.CTkButton(
    text="Upload CSV",
    image=upload_img,
    master=left_frame,
    command=upload_file,
    font=("Consolas", 16),
)
upload_csv_button.pack(
    padx=10,
    pady=10,
)


# for when the user successfully uploads or selects
# a valid csv dataset for their neural network
def open_training_window():
    # Clear the current widgets in the root window
    # destroy everyting except for the upload data pane
    for widget in right_frame.winfo_children():
        widget.destroy()

    for widget in root.winfo_children():
        widget.destroy()

    # add grid for hyper tuning neural network parameters


if __name__ == "__main__":
    root.mainloop()
