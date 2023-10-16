import tkinter as tk
from customtkinter import *


class App(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Backprop Playground")
        self.geometry("800x600")


if __name__ == "__main__":
    set_appearance_mode("system")
    app = App()
    app.mainloop()
