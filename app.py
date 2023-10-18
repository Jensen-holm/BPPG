from tkinter import messagebox
import customtkinter as ctk
import pandas as pd
from PIL import Image
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
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
upload = Image.open(os.path.join(ASSETS_DIR, "upload.png"))
logo = Image.open(os.path.join(ASSETS_DIR, "bppg.png"))
plus = Image.open(os.path.join(ASSETS_DIR, "plus.png"))
minus = Image.open(os.path.join(ASSETS_DIR, "minus.png"))

LOGO_IMG = ctk.CTkImage(
    light_image=logo,
    dark_image=logo,
    size=(400, 400),
)

UPLOAD_IMG = ctk.CTkImage(
    light_image=upload,
    dark_image=upload,
)

PLUS = ctk.CTkImage(
    light_image=plus,
    dark_image=plus,
)

MINUS = ctk.CTkImage(
    light_image=minus,
    dark_image=minus,
)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Backprop Playground")
        self.geometry(f"{1100}x{580}")
        self.minsize(width=600, height=300)
        self.eval("tk::PlaceWindow . center")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.test_button = ctk.CTkButton(
            master=self,
            image=LOGO_IMG,
            height=0,
            width=0,
            command=lambda:print(ARGS["data"]),
            text="",
        )

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
        self.sidebar_frame = ctk.CTkScrollableFrame(
            self, 
            width=250, 
            height=len(self.csvs) * 5,
            corner_radius=0,
        )
        self.sidebar_frame.grid(
            row=0,
            column=0,
            rowspan=len(self.csvs)+2, # + 1 for label and 1 for new file btn
            sticky="nsew",
        )
        self.sidebar_frame.rowconfigure(len(self.csvs), weight=1)
        self.upload_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Load CSV",
            font=("Consolas", 16),
        )
        self.upload_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # upload new csv button
        self.upload_new_csv = ctk.CTkButton(
            master=self.sidebar_frame,
            command=lambda: self.upload_new_csv,
            image=PLUS,
            text="Upload New CSV",
        )
        self.upload_new_csv.grid(row=1, column=0, padx=20, pady=(20, 10))

        # make 2 buttons for each csv, load() and remove()
        for i, csv in enumerate(self.csvs):
            i += 2
            label = ctk.CTkLabel(
                master=self.sidebar_frame,
                text=f"{csv[:10]}...",
            )
            label.grid(row=i, column=0, padx=2)

            load = ctk.CTkButton(
                master=self.sidebar_frame,
                text="",
                width=0,
                height=0,
                image=UPLOAD_IMG,
                command=lambda c=csv: self.use_csv(
                    filename=os.path.join(DATA_DIR, c),
                ),
            )
            load.grid(row=i, column=1, padx=2)

            remove = ctk.CTkButton(
                master=self.sidebar_frame,
                text="",
                width=0,
                height=0,
                image=MINUS,
                command=lambda c=csv: self.remove_csv(
                    filename=os.path.join(DATA_DIR, c),
                ),
            )
            remove.grid(row=i, column=2)

    # for using existing csv files
    def use_csv(self, filename: str):
        try:
            df = pd.read_csv(filename)
            ARGS["data"] = df
            self.update()
            return 
        except Exception as e:
            messagebox.showerror(
                title="CSV Reader Error",
                message=f"{e}",
            )
            return

    def remove_csv(self, filename) -> None:
        filepath = os.path.join(DATA_DIR, filename)
        os.remove(filepath)
        self.build_csv_upload_sidebar()
        return

    
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
            self.save_data(df, name=file.name)
            # if all was successful, use it!
            ARGS["data"] = df
            self.update()
            return

        except Exception as e:
            messagebox.showerror(
                title="CSV Reader Error",
                message=e, # might want to make this more readable in the future
            )
            return

    def save_data(self, df: pd.DataFrame, name: str) -> None:
        os.makedirs(DATA_DIR, exist_ok=True)
        base_name = os.path.basename(name)
        save_path = os.path.join(DATA_DIR, base_name)
        df.to_csv(save_path)
        self.update()
        return


if __name__ == "__main__":
    app = App()
    app.mainloop()
