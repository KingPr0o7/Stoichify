import tkinter as tk # Framework for GUI (Probably Install?)
import ttkbootstrap as ttk # Bootstrap theme for GUI (Need to install)

def convert():
	value = input_integer.get()
	output_string.set(value)

#
# Window Configuration
#   Define the window configuration; instance, title and size.
#

window = ttk.Window(themename= "darkly") # Initialize the window with the darkly theme
window.title("Stoichify")
window.geometry("800x600") # Window size (Width x Height)

#
# Elements within the window
#   Define the elements within the window; title, input form, submit button, output label.
#

# Title
title_label = ttk.Label(window, text="Stoichify", font="Arial 24 bold")
title_label.pack()

# Input Form, Submit Button, and Output Label linked to the convert function
input_frame = ttk.Frame(window)

input_integer = tk.IntVar()
input_form = ttk.Entry(input_frame, textvariable=input_integer)

submit_button = ttk.Button(input_frame, text="Submit", command=convert)

output_string = tk.StringVar()
output_label = ttk.Label(window, text="Output", font="Arial 12", textvariable=output_string)

# Pack said elements into the window
input_form.pack(side="left", padx=10)
submit_button.pack(side="left")
input_frame.pack(pady=10) 
output_label.pack(pady=10)

#
# Main Loop
#   Trigger execution for the main window loop
#

window.mainloop()