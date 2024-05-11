import tkinter as tk # Framework for GUI (Probably Install?)
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from entities import Equation, Substance
from sig_figs import Significant_Figures
import sv_ttk # Custom theme for ttk (https://github.com/rdbende/Sun-Valley-ttk-theme - pip install sv-ttk)
from PIL import Image, ImageTk # Pillow image library (pip install pillow)

class MainWindow:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("Stoichify")
		self.window.geometry("1000x725")
		sv_ttk.set_theme("dark")

		self.place_navbar(self.window)
		
		self.substances = []
		self.content = tk.Frame(self.window)
		self.content.pack(fill="both", expand=True)
  
		self.start(self.content)

	def reset(self):
		for child in self.content.winfo_children():
			child.destroy()
		self.input_frame.destroy()
		self.start(self.content)
  
	def place_navbar(self, frame):
		self.navbar = tk.Frame(frame, height=100)
		self.navbar.pack(side=tk.TOP, fill="x", padx=15)

		lines = tk.Frame(self.navbar, height=1, width=500)
		lines.pack(side=tk.BOTTOM, fill="x", expand=True)
		
		line1 = tk.Frame(lines, height=1,bg="white")
		line1.pack(side=tk.LEFT, fill="x", expand=True)
		
		self.exit = tk.Button(lines, text="Exit", command=self.window.quit, highlightthickness = 0, bd = 0, bg="red", fg="white", height=1, font=("Times New Roman", 13), width=10)
		self.exit.pack(side=tk.LEFT, padx=5)

		self.restart = tk.Button(lines, text="Restart", command=self.reset, highlightthickness = 0, bd = 0, bg="orange", fg="white", height=1, font=("Times New Roman", 13), width=10)
		self.restart.pack(side=tk.LEFT, padx=5)
		
		line2 = tk.Frame(lines, height=1, bg="white")
		line2.pack(side=tk.RIGHT, fill="x", expand=True)

		self.logoPath = 'images/stoichify_logo.png'
		self.logo = ImageTk.PhotoImage(Image.open(self.logoPath).resize((200, 81)))
		self.logo_size = tk.Label(self.navbar)
		self.logo_size.image = self.logo  # <== this is were we anchor the img object
		self.logo_size.configure(image=self.logo)
		self.logo_size.pack(side=tk.LEFT)

		self.extra_path = 'images/extra.png'
		self.extra = ImageTk.PhotoImage(Image.open(self.extra_path).resize((32, 32)))
		self.extra_size = tk.Button(self.navbar,command=lambda: messagebox.showinfo("Extra Page", "Extra options are not available yet."), highlightthickness = 0, bd = 0)
		self.extra_size.image = self.extra  # <== this is were we anchor the img object
		self.extra_size.configure(image=self.extra)
		self.extra_size.pack(side=tk.RIGHT)

		return self.navbar
  
	def start(self, frame):
		# Welcome Statement
		self.text_banner(frame, "Welcome to Stoichify!", "Built by Nathan Parker, with help from my chemistry teacher (Doctor of Philosophy in Chemistry) with the goal of simplifying the process of stoichiometry for beginner chemistry students. Please view the extra page for settings and credits of all contributors.")

		self.bottom_frame = tk.Frame(frame)
		self.bottom_frame.pack(side=tk.BOTTOM, fill="x", anchor="center")

		self.input_creator(self.bottom_frame, "dropdown", "Input Type:", 25, "stage_selection", ["Equation", "Substance Only"])
	
	def text_banner(self, frame, header, desc):
		self.banner_frame = tk.Frame(frame)
		self.banner_frame.pack(padx=15, pady=15, anchor="center", fill="y", expand=True)

		self.banner_header = ttk.Label(self.banner_frame, text=header, font=("Times New Roman", 25))
		self.banner_header.pack(pady=15, anchor="center")

		self.banner_text = ttk.Label(self.banner_frame, text=desc, font=("Times New Roman", 15), wraplength=800, justify='center')
		self.banner_text.pack(pady=15, anchor="center")		
 
	def input_creator(self, frame, type, tooltip, width, command=None, dropdown_options=None):
		self.input_frame = tk.Frame(frame)
		self.input_frame.pack(pady=15)

		self.input_explainer = ttk.Label(self.input_frame, text=tooltip, font=("Times New Roman", 15), width=15)
		self.input_explainer.pack(anchor="w", pady=5, padx=5)

		if type == "entry":
			self.input = ttk.Entry(self.input_frame, width=width)
			self.input.pack(side=tk.LEFT, padx=5)
		elif type == "dropdown":
			self.input = ttk.Combobox(self.input_frame, values=dropdown_options, width=width, state="readonly")
			self.input.pack(side=tk.LEFT, padx=5)

		self.submit = ttk.Button(self.input_frame, text="Submit")

		if command == "stage_selection":
			self.submit.config(command=lambda: self.stage_selector(self.input.get(), frame))
		elif command == "balance_equation":
			self.submit.config(command=lambda: self.balance(self.input.get(), "equation"))  
		elif command == "substance_only":
			self.submit.config(command=lambda: self.balance(self.input.get(), "substance"))
   
		self.submit.config(style="Accent.TButton")
		self.submit.pack(side=tk.LEFT, padx=5)

	def stage_selector(self, type, frame):
		self.banner_frame.destroy()
		self.input_frame.destroy()
     
		if type == "Equation":
			self.string = tk.StringVar()
			self.text_banner(self.content, "Inputting a Chemical Equation", "Since you chose “Equation Mode,” you need to type an equation CAREFULLY in the input below. Any mistyping will result in incorrect balancing, affecting the rest of the calculation. An example is: Fe + O2 → Fe2O3. For the formatting, include pluses between substances, correct element capitalization, all subscripts, an arrow of some sort (UNICODE or a dash and greater than “->”), and no charges (oxidation-reactions aren't supported).")
			self.input_creator(frame, "entry", "Equation:", 75, "balance_equation")
    
		elif type == "Substance Only":
			self.text_banner(self.content, "Inputting a Substance Only", "Since you chose “Substance Only Mode,” you need to type a substance CAREFULLY in the input below. An example is: H2O. For the formatting, include the correct element capitalization, all subscripts, and no charges")
			self.input_creator(frame, "entry", "Substance:", 25, "substance_only")

	def create_fraction(self, frame, numerator_text, denominator_text): 
		fraction_holder = tk.Frame(frame)
		fraction_holder.pack(side=tk.LEFT, padx=5, expand=True)
	
		max_length = max(len(numerator_text), len(denominator_text))
	
		numerator = tk.Label(fraction_holder, text=numerator_text, font=("Times New Roman", 20), width=max_length)
		numerator.pack(side=tk.TOP, anchor='center')
	
		line = tk.Frame(fraction_holder, height=1, width=200, bg="white")
		line.pack(side=tk.TOP, fill=tk.X, anchor='center')
	
		denominator = tk.Label(fraction_holder, text=denominator_text, font=("Times New Roman", 20), width=max_length)
		denominator.pack(side=tk.TOP, anchor='center')

	def balance(self, string, type):
		"""
		Balances the chemical equation using the Stoichify algorithm.
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
			self.banner_frame.destroy()
			self.last_phrase = ""
	
			# Fix this needs to come first
			if type == "equation":
				self.string = Equation(string)
				self.last_phrase = "Below is your balanced chemical equation, in which the coefficients will be used for the molar ratios:"
			elif type == "substance":
				self.string = Substance(string)
				self.last_phrase = "Below is your substance:"

			self.text_banner(self.content, "Doing the Stoichiometry", f"With a now fully balanced equation, you can start the stoichiometry process. For the given amount, you can enter an integer, float, or a number in scientific notation (Ex: “4.2 x 10^24” OR “4.2e24”). {self.last_phrase}")

			if type == "equation":
				self.showing_chemical_equation = tk.Label(self.content, text=self.string.balanced, font=("Times New Roman", 20))
				self.showing_chemical_equation.pack()

			elif type == "substance":
				self.showing_substance = tk.Label(self.content, text=self.string.calculation_presentation(), font=("Times New Roman", 20))
				self.showing_substance.pack()

			self.input_frame.destroy()

			self.input_frame = tk.Frame(self.window)
			self.input_frame.pack(side=tk.BOTTOM, pady=15, anchor="center")

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

			# Given substance
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

			# Wanted substance
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

			self.submit = ttk.Button(self.input_frame, text="Stoichify!", style="Accent.TButton", command=lambda: self.stoichiometry_inputs_checker(type))
			self.submit.pack(side=tk.BOTTOM, pady=15, fill=tk.X)
  
		# self.submit.config(command=lambda: self.stoichiometry_inputs_checker())
  
	def stoichiometry_inputs_checker(self, type):
		"""
		Checks if the user inputted valid values for stoichiometry calculations.
		"""
		given_amount = self.given_amount.get()
		given_significant_figures = Significant_Figures().parser(given_amount)[0]
		given_measurement = self.given_measurement.get()
		given_substance = self.given_substance.get()
		wanted_measurement = self.wanted_measurement.get()
		wanted_substance = self.wanted_substance.get()
  
		if given_measurement not in ["g", "mol", "L", "r.p."]:
			return messagebox.showerror("Given Measurement Left Blank", "The given measurement was left blank. Please select a valid measurement.")
  
		if type == "equation" and given_substance not in self.string.substances:
			return messagebox.showerror("Given Substance Left Blank", "The given substance was left blank. Please select a valid substance.")
  
		if wanted_measurement not in ["g", "mol", "L", "r.p."]:
			return messagebox.showerror("Wanted Measurement Left Blank", "The wanted measurement is was left blank. Please select a valid measurement.")
  
		if type == "equation" and wanted_substance not in self.string.substances:
			return messagebox.showerror("Wanted Substance Left Blank", "The wanted substance is was left blank. Please select a valid substance.")
  
		self.string.stoichify(given_amount, given_significant_figures, given_measurement, given_substance, wanted_measurement, wanted_substance)

		self.banner_frame.destroy()
		if type == "equation":
			self.showing_chemical_equation.destroy()
		elif type == "substance":
			self.showing_substance.destroy()
		self.input_frame.destroy()

		if type == "equation":
			self.phrase = "balanced chemical equation"
		elif type == "substance":
			self.phrase = "substance"

		self.text_banner(self.content, "Stoichiometry Results", f"Below is the completed calculation! This includes the final {self.phrase}, and the conversion from the given to the wanted. All shown out like you would write on a piece of paper. If this calculation is wrong, please go to the extra page and report an issue.")

		if type == "equation":
			self.showing_chemical_equation = tk.Label(self.content, text=self.string.balanced, font=("Times New Roman", 20))
			self.showing_chemical_equation.place(relx=0.5, rely=0.4, anchor='center')
		
		elif type == "substance":
			self.showing_substance = tk.Label(self.content, text=self.string.calculation_presentation(), font=("Times New Roman", 20))
			self.showing_substance.place(relx=0.5, rely=0.4, anchor='center')        
		
		self.work_shown_wrapper = ttk.Frame(self.content, width=500, style="Accent.TFrame")
		self.work_shown_wrapper.place(relx=0.5, rely=0.5, anchor='center')
  
		for index, fraction in enumerate(self.string.work_shown):
			if isinstance(fraction, str):
				label = tk.Label(self.work_shown_wrapper, text=fraction, font=("Times New Roman", 20))
				label.pack(side=tk.LEFT, padx=5)
			elif isinstance(fraction, tuple):
				self.create_fraction(self.work_shown_wrapper, fraction[0], fraction[1])
				if index+1 < len(self.string.work_shown) and isinstance(self.string.work_shown[index+1], tuple):
					label = tk.Label(self.work_shown_wrapper, text="×", font=("Times New Roman", 20))
					label.pack(side=tk.LEFT, padx=5) 


	def run(self):
		self.window.mainloop()

if __name__ == "__main__":
	# C3H8 + O2 → CO2 + H2O
	# 0238974C3H8 + 0239874O2 → 09248357CO2 + 824937H2O
	main_window = MainWindow()
	main_window.run()