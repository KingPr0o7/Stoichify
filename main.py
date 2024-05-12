#
# Nathan Parker | 5/11/24 | v0.8.0
# Stoichify - A stoichiometry calculator for beginner chemistry students.
# Built and designed for ease-of-use, Stoichify aims to give students via a GUI/UI
# that is easy to digest, input, and see the work of the program. Stoichify consists
# of 4 modules that handle the GUI, equations and substances, stoichiometric calculations,
# and precision of values. This file (main.py) is responsible for the GUI creation, input 
# handling, and output gathering from all other files. From creating the window, to showing 
# the results, this file is critical for the user experience and makes Stoichify into a 
# user-friendly program.
#
# Main Libraries:
# - tkinter: Framework for GUI (ttk for custom widgets)
# - sv_ttk: Custom theme for ttk (Sun-Valley-ttk-theme - https://github.com/rdbende/Sun-Valley-ttk-theme)
# - PIL: Image library for Python (Pillow - https://pillow.readthedocs.io/en/stable/)
#

# GUI Libraries
import tkinter as tk # Framework for GUI (Probably Install?)
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
import sv_ttk # Custom theme for ttk (https://github.com/rdbende/Sun-Valley-ttk-theme - pip install sv-ttk)
from PIL import Image, ImageTk # Pillow image library (pip install pillow)

# Logical Libraries
from entities import Equation, Substance
from precision import Significant_Figures

class MainWindow:
	"""
	Initializes the main window of Stoichify, with pre-set window geometry, title, etc.
	With methods pertaining to the GUI handling, e.g. resting, placing the navbar, stage
	selection, creating inputs, balancing equations, stoichiometry calculations, etc. 
	"""

	def __init__(self):
		# Create Window
		self.window = tk.Tk()
		self.window.title("Stoichify")
		self.window.geometry("1000x725")
		sv_ttk.set_theme("dark")

		# Create top and bottom frames
		self.place_navbar()
		self.content = tk.Frame(self.window) # Content is the interaction/display frame
		self.content.pack(fill="both", expand=True)
  
		self.start() # Show text banner and input type selector 

	def place_navbar(self):
		"""
		Creates the navbar at the top of the window, with the Stoichify logo, extra button,
		and the exit and restart buttons. The navbar is always present at the top of the window,
		and is never destroyed or re-created.
  
		:return: Stoichify's Navbar (Consisting of the logo, extra button, exit, and restart buttons)
		"""

		# Navbar Frame
		self.navbar = tk.Frame(self.window, height=100)
		self.navbar.pack(side=tk.TOP, fill="x", padx=15)

		# Lines' Frame (Located under the navbar that separates the navbar from the content and emphasizes exit and restart buttons)
		lines = tk.Frame(self.navbar, height=1, width=500)
		lines.pack(side=tk.BOTTOM, fill="x", expand=True)
		
		line_left = tk.Frame(lines, height=1,bg="white")
		line_left.pack(side=tk.LEFT, fill="x", expand=True)
		
		# The required exit button to kill Stoichify
		self.exit = tk.Button(lines, text="Exit", command=self.window.quit, highlightthickness = 0, bd = 0, bg="red", fg="white", height=1, font=("Times New Roman", 13), width=10)
		self.exit.pack(side=tk.LEFT, padx=5)

		# The restart button calls the reset method to clear all widgets and re-create the start screen 
		self.restart = tk.Button(lines, text="Restart", command=self.reset, highlightthickness = 0, bd = 0, bg="orange", fg="white", height=1, font=("Times New Roman", 13), width=10)
		self.restart.pack(side=tk.LEFT, padx=5)
		
		line_right = tk.Frame(lines, height=1, bg="white")
		line_right.pack(side=tk.RIGHT, fill="x", expand=True)

		try:
			self.logo = ImageTk.PhotoImage(Image.open(self.logoPath).resize((200, 81)))
		except Exception as e:
			self.logo_size = tk.Label(self.navbar, text="Stoichify Main Logo") # ALT Text
		else:
			self.logo_size = tk.Label(self.navbar)
			self.logo_size.image = self.logo # Save the image to prevent garbage collection
			self.logo_size.configure(image=self.logo)
		finally:
			self.logo_size.pack(side=tk.LEFT)

		# Extra Button (Top Right of the Navbar - Opens required second window for information and settings)
		try:
			self.extra = ImageTk.PhotoImage(Image.open(self.extra_path).resize((32, 32)))
		except Exception as e:
			self.extra_size = tk.Button(self.navbar, text="Extra Page", command=lambda: messagebox.showinfo("Extra Page", "Extra options are not available yet."), highlightthickness = 0, bd = 0)
		else:
			self.extra_size = tk.Button(self.navbar, command=lambda: messagebox.showinfo("Extra Page", "Extra options are not available yet."), highlightthickness = 0, bd = 0)
			self.extra_size.image = self.extra  # Save the image to prevent garbage collection
			self.extra_size.configure(image=self.extra)
		finally:
			self.extra_size.pack(side=tk.RIGHT)

		return self.navbar	

	def start(self):
		"""
		The "start" stage, where the user is greeted with a welcome message 
		and asked to select their input type (Equation or Substance Only).
		This method only ADDS widgets to the window, it does not destroy any.
		Use the reset method to clear all widgets and re-create the start screen.
  
		:return: Stoichify's Main/Start Window
		"""

		# Welcome Statement
		self.text_banner("Welcome to Stoichify!", "Built by Nathan Parker, with help from my chemistry teacher (Doctor of Philosophy in Chemistry) with the goal of simplifying the process of stoichiometry for beginner chemistry students. Please view the extra page for settings and credits of all contributors.")

		self.bottom_frame = tk.Frame(self.content)
		self.bottom_frame.pack(side=tk.BOTTOM, fill="x", anchor="center")

		self.input_creator(self.bottom_frame, "dropdown", "Input Type:", 25, "stage_selection", ["Equation", "Substance Only"])

	def reset(self):
		"""
		Resets the window to the start, clearing all widgets and 
		re-creating (not killing the window) the start screen. 
		Only triggered upon clicking the restart button in the navbar.
  
		:return: Stoichify's Main/Start Window
		"""
     
		for child in self.content.winfo_children(): # Vanish all children
			child.destroy()
		self.input_frame.destroy()
		self.start() # Go back to start layout

	def text_banner(self, header, desc):
		"""
		Creates a text banner with a header and description, at the
		top of the window. This banner is used to display information
		to the user about the current stage of the program, and other
		instructions.
  
		:param header: The header of the banner
		:param desc: The description of the banner (only one line, it will wrap if too long)
		:return: Stoichify's Text Banner
		"""

		self.banner_frame = tk.Frame(self.content)
		self.banner_frame.pack(padx=15, pady=15, anchor="center", fill="y", expand=True)

		self.banner_header = ttk.Label(self.banner_frame, text=header, font=("Times New Roman", 25))
		self.banner_header.pack(pady=15, anchor="center")

		self.banner_text = ttk.Label(self.banner_frame, text=desc, font=("Times New Roman", 15), wraplength=800, justify='center')
		self.banner_text.pack(pady=15, anchor="center")		
 
		return self.banner_frame
 
	def stage_selector(self, stage, frame):
		"""
		Destroys the current frame contents, and goes to the next
		stage based on the user's selection. The stages are either
		"Equation" or "Substance Only", leading to different
		logical paths in the program.
  
		:param stage: The user's selection of the next stage
		:param frame: The frame to place the input in
		:return: The next stage specified by the user
		"""

		self.banner_frame.destroy()
		self.input_frame.destroy()
     
		# Selects the stage, equations require slightly different logic
		if stage == "Equation":
			self.string = tk.StringVar()
			self.text_banner("Inputting a Chemical Equation", "Since you chose “Equation Mode,” you need to type an equation CAREFULLY in the input below. Any mistyping will result in incorrect balancing, affecting the rest of the calculation. An example is: Fe + O2 → Fe2O3. For the formatting, include pluses between substances, correct element capitalization, all subscripts, an arrow of some sort (UNICODE or a dash and greater than “->”), and no charges (oxidation-reactions aren't supported).")
			self.input_creator(frame, "entry", "Equation:", 75, "balance_equation")
    
		elif stage == "Substance Only":
			self.text_banner("Inputting a Substance Only", "Since you chose “Substance Only Mode,” you need to type a substance CAREFULLY in the input below. An example is: H2O. For the formatting, include the correct element capitalization, all subscripts, and no charges")
			self.input_creator(frame, "entry", "Substance:", 25, "substance_only")
 
	def input_creator(self, frame, type, tooltip, width, stage=None, dropdown_options=None):
		"""
		A shorthand function to create inputs with a frame, explainer (tooltip),
		and they input (based on type - entry or dropdown). With a submit button;
		usually only for one input creation. After the checks clear, inputs are 
		cleared, and the next stage is shown with inputs for stoichiometry 
		(not using the input_creator). 
  
		:param frame: The frame to place the input in
		:param type: The type of input (entry or dropdown)
		:param tooltip: The explainer text for the input
		:param width: The width of the input (applies to both types)
		:param stage: The current stage to apply it's command to the submit button 
		:param dropdown_options: The options for the dropdown (only for dropdown type)
		:return: A input with a explainer, input, and submit button
		"""

		# Create the input frame
		self.input_frame = tk.Frame(frame)
		self.input_frame.pack(pady=15)

		# Add explainer text
		self.input_explainer = ttk.Label(self.input_frame, text=tooltip, font=("Times New Roman", 15), width=15)
		self.input_explainer.pack(anchor="w", pady=5, padx=5)

		# Create the input based on the type
		if type == "entry":
			self.input = ttk.Entry(self.input_frame, width=width)
			self.input.pack(side=tk.LEFT, padx=5)
		elif type == "dropdown":
			self.input = ttk.Combobox(self.input_frame, values=dropdown_options, width=width, state="readonly")
			self.input.pack(side=tk.LEFT, padx=5)

		self.submit = ttk.Button(self.input_frame, text="Submit")

		# Change the command based on current stage
		if stage == "stage_selection":
			self.submit.config(command=lambda: self.stage_selector(self.input.get(), frame))
		elif stage == "balance_equation":
			self.submit.config(command=lambda: self.balance(self.input.get(), "equation"))  
		elif stage == "substance_only":
			self.submit.config(command=lambda: self.balance(self.input.get(), "substance"))
   
		# Style the submit button
		self.submit.config(style="Accent.TButton")
		self.submit.pack(side=tk.LEFT, padx=5)
  
		return self.input_frame

	def balance(self, string, type):
		"""
		Calls entities.py to balance and create the equation or create a substance object
		from the user's input. Upon the call of such, errors are caught and displayed
		via a messagebox. 
		"""

		try:
			if type == "equation":
				self.string = Equation(string)
			elif type == "substance":
				self.string = Substance(string)
		except Exception as e:
			error_string = str(e)
			if ":" in error_string:
				error_string = error_string.split(":")
				return messagebox.showerror(error_string[0], error_string[1])
			else:
				return messagebox.showerror("Error Occurred - UNKNOWN", e)
		else:
			# Clear the banner
			self.banner_frame.destroy()
			self.last_phrase = ""

			# Change the phrase based on the type (equation or substance), I wanted this to be as specific as possible
			if type == "equation":
				self.last_phrase = "Below is your balanced chemical equation, in which the coefficients will be used for the molar ratios:"
			elif type == "substance":
				self.last_phrase = "Below is your substance:"

			self.text_banner("Doing the Stoichiometry", f"With a now fully balanced equation, you can start the stoichiometry process. For the given amount, you can enter an integer, float, or a number in scientific notation (Ex: “4.2 x 10^24” OR “4.2e24”). {self.last_phrase}")

			# Based on the type, show either the fully balanced equation or the just the substance
			if type == "equation":
				self.showing_chemical_equation = tk.Label(self.content, text=self.string.balanced, font=("Times New Roman", 20))
				self.showing_chemical_equation.pack()

			elif type == "substance":
				self.showing_substance = tk.Label(self.content, text=self.string.calculation_presentation(), font=("Times New Roman", 20))
				self.showing_substance.pack()

			# Destroy and create the input frame for the stoichiometry inputs
			self.input_frame.destroy()
			self.input_frame = tk.Frame(self.window)
			self.input_frame.pack(side=tk.BOTTOM, pady=15, anchor="center")

			#
			# Stoichiometry Inputs
			#   These contain all required inputs for the stoichiometry calculations.	
			#   All with their own explainer and input, with a submit button at the end.
			#

			# Given amount
			frame_given_amount = tk.Frame(self.input_frame)
			frame_given_amount.pack(side=tk.TOP, fill=tk.X)
			self.given_amount_explainer = ttk.Label(frame_given_amount, text="Given Amount?", font=("Times New Roman", 15), width=25)
			self.given_amount_explainer.pack(side=tk.LEFT)
			self.given_amount = ttk.Entry(frame_given_amount, width=20)
			self.given_amount.pack(side=tk.LEFT, padx=5)

			# Given measurement
			frame_given_measurement = tk.Frame(self.input_frame)
			frame_given_measurement.pack(side=tk.TOP, fill=tk.X)
			self.given_measurement_explainer = ttk.Label(frame_given_measurement, text="Given Measurement Unit?", font=("Times New Roman", 15), width=25)
			self.given_measurement_explainer.pack(side=tk.LEFT)
			self.given_measurement = ttk.Combobox(frame_given_measurement, values=["g", "mol", "L", "r.p."], width=15, state="readonly")
			self.given_measurement.pack(side=tk.LEFT, padx=5)

			# Given substance (substance mode is only one substance, equation mode is multiple substances)
			if type == "equation":
				frame_given_substance = tk.Frame(self.input_frame)
				frame_given_substance.pack(side=tk.TOP, fill=tk.X)
				self.given_substance_explainer = ttk.Label(frame_given_substance, text="Given Substance?", font=("Times New Roman", 15), width=25)
				self.given_substance_explainer.pack(side=tk.LEFT)
				self.given_substance = ttk.Combobox(frame_given_substance, values=self.string.substances, width=15, state="readonly")
				self.given_substance.pack(side=tk.LEFT, padx=5)

			elif type == "substance":
				frame_given_substance = tk.Frame(self.input_frame)
				frame_given_substance.pack(side=tk.TOP, fill=tk.X)
				self.given_substance_explainer = ttk.Label(frame_given_substance, text="Given Substance?", font=("Times New Roman", 15), width=25)
				self.given_substance_explainer.pack(side=tk.LEFT)
				self.given_substance = ttk.Combobox(frame_given_substance, values=[self.string.substance], width=15, state="readonly")
				self.given_substance.current(0)
				self.given_substance.pack(side=tk.LEFT, padx=5)

			# Wanted measurement
			frame_wanted_measurement = tk.Frame(self.input_frame)
			frame_wanted_measurement.pack(side=tk.TOP, fill=tk.X)
			self.wanted_measurement_explainer = ttk.Label(frame_wanted_measurement, text="Wanted Measurement Unit?", font=("Times New Roman", 15), width=25)
			self.wanted_measurement_explainer.pack(side=tk.LEFT)
			self.wanted_measurement = ttk.Combobox(frame_wanted_measurement, values=["g", "mol", "L", "r.p."], width=15, state="readonly")
			self.wanted_measurement.pack(side=tk.LEFT, padx=5)

			# Wanted substance (substance mode is only one substance, equation mode is multiple substances)
			if type == "equation":
				frame_wanted_substance = tk.Frame(self.input_frame)
				frame_wanted_substance.pack(side=tk.TOP, fill=tk.X)
				self.wanted_substance_explainer = ttk.Label(frame_wanted_substance, text="Wanted Substance?", font=("Times New Roman", 15), width=25)
				self.wanted_substance_explainer.pack(side=tk.LEFT)
				self.wanted_substance = ttk.Combobox(frame_wanted_substance, values=self.string.substances, width=15, state="readonly")
				self.wanted_substance.pack(side=tk.LEFT, padx=5)
	
			elif type == "substance":
				frame_wanted_substance = tk.Frame(self.input_frame)
				frame_wanted_substance.pack(side=tk.TOP, fill=tk.X)
				self.wanted_substance_explainer = ttk.Label(frame_wanted_substance, text="Wanted Substance?", font=("Times New Roman", 15), width=25)
				self.wanted_substance_explainer.pack(side=tk.LEFT)
				self.wanted_substance = ttk.Combobox(frame_wanted_substance, values=[self.string.substance], width=15, state="readonly")
				self.wanted_substance.current(0)
				self.wanted_substance.pack(side=tk.LEFT, padx=5)

			# Submit button to check all inputs
			self.submit = ttk.Button(self.input_frame, text="Stoichify!", style="Accent.TButton", command=lambda: self.stoichify(type))
			self.submit.pack(side=tk.BOTTOM, pady=15, fill=tk.X)

	def create_fraction(self, frame, numerator_text, denominator_text): 
		"""
		A custom fraction creator to display all values/work as would be
		shown on a piece of paper. So that the user can see the work blown
		out, instead of just showing an answer. Each fraction has it's numerator
		and denominator, with a line in-between (1/1 fractions are disregarded in
  		stoichiometry.py).
	
		:param frame: The frame to place the fraction in
		:param numerator_text: The numerator of the fraction
		:param denominator_text: The denominator of the fraction
		:return: A fraction with a numerator, denominator, and line in-between to be placed in the work_shown
		"""

		# Create the fraction holder (numerator, line, denominator)
		fraction_holder = tk.Frame(frame)
		fraction_holder.pack(side=tk.LEFT, padx=5, expand=True)

		max_length = max(len(numerator_text), len(denominator_text)) # Set the width of the fraction based on the longest string
	
		# Top part of the fraction (numerator)
		numerator = tk.Label(fraction_holder, text=numerator_text, font=("Times New Roman", 20), width=max_length)
		numerator.pack(side=tk.TOP, anchor='center')
	
		# Line in-between the numerator and denominator (to actually make it a fraction)
		line = tk.Frame(fraction_holder, height=1, width=200, bg="white")
		line.pack(side=tk.TOP, fill=tk.X, anchor='center')
	
		# Bottom part of the fraction (denominator)
		denominator = tk.Label(fraction_holder, text=denominator_text, font=("Times New Roman", 20), width=max_length)
		denominator.pack(side=tk.TOP, anchor='center')
  
		return fraction_holder
  
	def stoichify(self, type):
		"""
		Checks all the stoichiometry inputs (created by balance), 
		calls the stoichify method, and recreates the display of 
		the equation/substance, then shows the work shown as a
		student would write it on a piece of paper.

		:param type: The type of input (equation or substance)
		:return: Stoichiometry Results (Balanced Equation, Work Shown, etc.)
		"""

		#
		# The Deal With Significant Figures
		#   Tkinter saves a exact string representation of the number, 
  		#   thus all digits (including trailing zeros) are saved. From
		#   this we can count the significant figures of the given amount.
		#

		given_amount = self.given_amount.get()
		given_significant_figures = Significant_Figures().parser(given_amount)

		# Get all other inputs 
		given_measurement = self.given_measurement.get()
		given_substance = self.given_substance.get()
		wanted_measurement = self.wanted_measurement.get()
		wanted_substance = self.wanted_substance.get()
  
		#
		# Error Checking	
		#   Checks to see if any inputs were left blank, and throws error messages if so.
		#	

		if given_measurement not in ["g", "mol", "L", "r.p."]:
			return messagebox.showerror("Given Measurement Left Blank", "The given measurement was left blank. Please select a valid measurement.")
  
		if type == "equation" and given_substance not in self.string.substances:
			return messagebox.showerror("Given Substance Left Blank", "The given substance was left blank. Please select a valid substance.")
  
		if wanted_measurement not in ["g", "mol", "L", "r.p."]:
			return messagebox.showerror("Wanted Measurement Left Blank", "The wanted measurement is was left blank. Please select a valid measurement.")
  
		if type == "equation" and wanted_substance not in self.string.substances:
			return messagebox.showerror("Wanted Substance Left Blank", "The wanted substance is was left blank. Please select a valid substance.")
  
		# Call the stoichify method from entities.py (changes based on type - equation or substance)
		self.string.stoichify(given_amount, given_significant_figures, given_measurement, given_substance, wanted_measurement, wanted_substance)

		# Destroy the banner, substance/equation, and input frame
		self.banner_frame.destroy()
		if type == "equation":
			self.showing_chemical_equation.destroy()
			self.phrase = "balanced chemical equation"
		elif type == "substance":
			self.showing_substance.destroy()
			self.phrase = "substance"
		self.input_frame.destroy()

		# Explain to the user what the results
		self.text_banner("Stoichiometry Results", f"Below is the completed calculation! This includes the final {self.phrase}, and the conversion from the given to the wanted. All shown out like you would write on a piece of paper. If this calculation is wrong, please go to the extra page and report an issue.")

		if type == "equation":
			self.showing_chemical_equation = tk.Label(self.content, text=self.string.balanced, font=("Times New Roman", 20))
			self.showing_chemical_equation.place(relx=0.5, rely=0.4, anchor='center')
		
		elif type == "substance":
			self.showing_substance = tk.Label(self.content, text=self.string.calculation_presentation(), font=("Times New Roman", 20))
			self.showing_substance.place(relx=0.5, rely=0.4, anchor='center')        

		#
		# Work Shown
		#   Create the wrapper for the work shown, and loop throught the
		#   work_shown list to display the work as a student would write it.
		#		
  
		self.work_shown_wrapper = ttk.Frame(self.content, width=500, style="Accent.TFrame")
		self.work_shown_wrapper.place(relx=0.5, rely=0.5, anchor='center')
  
		for index, fraction in enumerate(self.string.work_shown):
			# If it's a string it's a given or answer
			if isinstance(fraction, str):
				label = tk.Label(self.work_shown_wrapper, text=fraction, font=("Times New Roman", 20))
				label.pack(side=tk.LEFT, padx=5)
			# If it's a tuple it's a fraction (like molar bridge or conversions)
			elif isinstance(fraction, tuple):
				self.create_fraction(self.work_shown_wrapper, fraction[0], fraction[1])
				if index+1 < len(self.string.work_shown) and isinstance(self.string.work_shown[index+1], tuple):
					label = tk.Label(self.work_shown_wrapper, text="×", font=("Times New Roman", 20))
					label.pack(side=tk.LEFT, padx=5) 

	def run(self):
		"""
		Runs the main window of Stoichify, with the mainloop method
		which keeps the window open until the user closes it via
		the exit button in the navbar.
  
		:return: Starts the main window process of Stoichify
		"""

		self.window.mainloop()

if __name__ == "__main__":
	# C3H8 + O2 → CO2 + H2O
	# 0238974C3H8 + 0239874O2 → 09248357CO2 + 824937H2O
	main_window = MainWindow()
	main_window.run()