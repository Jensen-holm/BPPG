import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("system")

root = ctk.CTk()
root.geometry("800x600")
root.title("Backprop Playground")

button = ctk.CTkButton(
    master=root,
    text="train",
)

button.place(
    relx=0.5,
    rely=0.5,
    anchor=tk.CENTER,
)

if __name__ == "__main__":
    root.mainloop()
