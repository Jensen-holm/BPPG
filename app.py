import tkinter as tk
import customtkinter as ctk
import PIL

ctk.set_appearance_mode("system")

root = ctk.CTk()
root.geometry("800x600")
root.title("Backprop Playground")
root.minsize(600, 400)


upload = PIL.Image.open("assets/upload.png")
upload_img = ctk.CTkImage(
    light_image=upload,
    dark_image=upload,
)

upload_csv_button = ctk.CTkButton(
    text="upload csv",
    image=upload_img,
    master=root,
)

upload_csv_button.place(
    relx=0.5,
    rely=0.5,
    anchor=tk.CENTER,
)

if __name__ == "__main__":
    root.mainloop()
