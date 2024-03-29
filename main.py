import tkinter as tk # Framework for GUI (Probably Install?)
from tkinter import ttk
import sv_ttk # Custom theme for ttk (https://github.com/rdbende/Sun-Valley-ttk-theme - pip install sv-ttk)
from PIL import Image, ImageTk # Pillow image library (pip install pillow)

#
# Window Configuration
#   Define the window configuration; instance, title and size.
#

window = tk.Tk()
window.title("Stoichify")
window.geometry("1600x900") # Window size (Width x Height)
sv_ttk.set_theme("dark") # Set Sun Valley to dark mode

#
# Elements within the window
#   Define the elements within the window; navbar, logo, label and button.
#

navbar = ttk.Frame(window)
navbar.pack(side="top", fill="x")

logo = Image.open("images/stoichify_logo.png").resize((200, 81))
logo_tk = ImageTk.PhotoImage(logo)

label = ttk.Label(navbar, text="Stoichify", image=logo_tk)
label.pack(side="left", padx=10)

button = ttk.Button(window, text="Click me!")
button.pack()

#
# Main Loop
#   Trigger execution for the main window loop
#

window.mainloop()