import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import pandas as pd
from PIL import Image
import os

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

BASE_DIR = os.path.dirname(__file__)
ARGS = {
    "epochs": 1000, # int greater than 1 
    "hidden_size": 8, # positive even int
    "learning_rate": 0.01, # float between 0 and 1
    "test_size": 0.2, # float between 0 and 1
    "activation": "relu", # string that'll be mapped to func
    "features": [], # list of strings in data cols
    "target": "", # string that's in data cols 
    "data": None, # pandas data frame
}

# loading images
upload = Image.open(os.path.join(BASE_DIR, "assets/upload.png"))
logo = Image.open(os.path.join(BASE_DIR, "assets/backprop_playground.png"))

LOGO_IMG = ctk.CTkImage(
    light_image=logo,
    dark_image=logo,
)

UPLOAD_IMG = ctk.CTkImage(
    light_image=upload,
    dark_image=upload,
)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Backprop Playground")
        self.geometry(f"{1100}x{580}")
        self.minsize(width=600, height=300)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.csvs = self.csv_files()
        self.build_csv_upload_sidebar()


    """ CSV upload side bar """
    def csv_files(self):
        data_path = os.path.join(BASE_DIR, "data")
        csvs = []
        for f in os.listdir(data_path):
            if self.is_csv_file(f):
                csvs.append(f)
        return csvs

    @staticmethod
    def is_csv_file(f_name: str) -> bool:
        file_extension = os.path.splitext(f_name)[-1]
        return file_extension.lower() == ".csv"

    def build_csv_upload_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(
            self, 
            width=140, 
            corner_radius=0,
        )
        self.sidebar_frame.grid(
            row=0,
            column=0,
            rowspan=len(self.csvs)+1,
            sticky="nsew",
        )
        self.sidebar_frame.rowconfigure(4, weight=1)
        self.upload_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Load CSV",
            font=("Consolas", 16),
        )
        self.upload_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # upload new csv button
        self.upload_new_csv = ctk.CTkButton(
            master=self.sidebar_frame,
            command=self.upload_new_csv,
            image=UPLOAD_IMG, 
        )
        self.upload_new_csv.grid(row=1, column=0, padx=20, pady=(20, 10))

    
    def upload_new_csv(self) -> None:
        file = ctk.filedialog.askopenfile()
        if not file:
            return
        
        if not self.is_csv_file(f_name=file.name):
            ext = os.path.splitext(file.name)[-1]
            messagebox.showerror(
                title="Invalid File Type",
                message=f"You tried uploading a \"{ext}\" file but only CSV files are allowed",
            )
            return
        
        try: # try to read the csv file & save it to /data...
            df = pd.read_csv(file)
            ARGS["data"] = df

            save_dir = os.path.join(os.getcwd(), "data")
            os.makedirs(save_dir, exist_ok=True)  # ensure 'data' folder exists
            save_path = os.path.join(save_dir, os.path.basename(file.name))
            df.to_csv(save_path)
            return

        except Exception as e:
            messagebox.showerror(
                title="CSV Reader Error",
                message=e, # might want to make this more readable in the future
            )
            return


if __name__ == "__main__":
    app = App()
    app.mainloop()
