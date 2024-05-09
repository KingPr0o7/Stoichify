import tkinter as tk # Framework for GUI (Probably Install?)
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from entities import Equation
from sig_figs import Significant_Figures
import sv_ttk # Custom theme for ttk (https://github.com/rdbende/Sun-Valley-ttk-theme - pip install sv-ttk)
from PIL import Image, ImageTk # Pillow image library (pip install pillow)

class MainWindow:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("Stoichify")
		self.window.geometry("1000x700")
		
		self.substances = []
		self.content = tk.Frame(self.window)
		self.content.pack(fill="both", expand=True)
		# ---------------
		sv_ttk.set_theme("dark")

		self.enter_equation_stage()

	def enter_equation_stage(self):
		self.equation = tk.StringVar()

		self.place_navbar(self.content)
  
		self.welcome_frame = tk.Frame(self.content)
		self.welcome_frame.pack(padx=15, pady=15, anchor="center", fill="y", expand=True)

		self.welcome = ttk.Label(self.welcome_frame, text="Welcome to Stoichify!", font=("Times New Roman", 25))
		self.welcome.pack(pady=15, anchor="center")

		self.welcome_text = ttk.Label(self.welcome_frame, text="Built by Nathan Parker, with help from my chemistry teacher (Doctor of Philosophy in Chemistry) with the goal of simplifying the process of stoichiometry for beginner chemistry students. Please view the extra page for settings and credits of all contributors.", font=("Times New Roman", 15), wraplength=800, justify='center')
		self.welcome_text.pack(pady=15, anchor="center")

		# ---
		self.user_input = ttk.Frame(self.content, height=10)
		self.user_input.pack(side=tk.BOTTOM, pady=15)

		self.input_type_frame = ttk.Frame(self.user_input)
		self.input_type_frame.pack(side=tk.LEFT, pady=15)

		self.input_type_explainer = ttk.Label(self.input_type_frame, text="Input Type:", font=("Times New Roman", 15), width=15)
		self.input_type_explainer.pack(anchor="w", pady=5, padx=5)

		self.input_type = ttk.Combobox(self.input_type_frame, values=["Equation", "Substance Only"], width=15, state="readonly")
		self.input_type.pack(side=tk.LEFT, padx=5)

		# self.equation_input_frame = ttk.Frame(self.user_input)
		# self.equation_input_frame.pack(side=tk.LEFT, pady=15)

		# self.equation_input_explainer = ttk.Label(self.equation_input_frame, text="Equation (Unbalanced or Balanced):", font=("Times New Roman", 15))
		# self.equation_input_explainer.pack(side=tk.TOP, pady=5)

		# self.equation_and_submit_frame = ttk.Frame(self.equation_input_frame)
		# self.equation_and_submit_frame.pack(side=tk.TOP)

		# self.equation_input = ttk.Entry(self.equation_and_submit_frame, textvariable=self.equation, width=75)
		# self.equation_input.pack(side=tk.LEFT, padx=5)

		self.submit = ttk.Button(self.input_type_frame, text="Submit", command=lambda: self.balance_equation(self.equation.get()))
		self.submit.config(style="Accent.TButton")
		self.submit.pack(side=tk.LEFT, padx=5)

	def reset(self):
		for child in self.content.winfo_children():
			child.destroy()
		self.enter_equation_stage()

	def place_navbar(self, frame):
		self.navbar = tk.Frame(frame, height=100)
		self.navbar.pack(side=tk.TOP, fill="x", padx=15)

		lines = tk.Frame(self.navbar, height=1, width=500)
		lines.pack(side=tk.BOTTOM, fill="x", expand=True)
		
		line1 = tk.Frame(lines, height=1,bg="white")
		line1.pack(side=tk.LEFT, fill="x", expand=True)
		
		self.exit = tk.Button(lines, text="Exit", command=self.content.quit, highlightthickness = 0, bd = 0, bg="red", fg="white", height=1, font=("Times New Roman", 13), width=10)
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

	def balance_equation(self, equation):
		"""
		Balances the chemical equation using the Stoichify algorithm.
		"""
		self.equation = Equation(equation)

		showing_chemical_equation = tk.Label(self.content, text=self.equation.balanced, font=("Times New Roman", 20))
		showing_chemical_equation.pack()

		self.work_shown_wrapper = ttk.Frame(self.content, width=500, style="Accent.TFrame")
		self.work_shown_wrapper.pack(pady=15, anchor="center")

		self.equation_input.destroy()
		self.given_amount = ttk.Entry(self.user_input, width=25)
		self.given_amount.pack(side=tk.LEFT, fill="y")
  
		self.given_measurement = ttk.Combobox(self.user_input, values=["g", "mol", "L", "r.p."], width=15, state="readonly")
		self.given_measurement.pack(side=tk.LEFT, padx=5, fill="y")
  
		self.sentence_break_of = ttk.Label(self.user_input, text="of", font=("Times New Roman", 20))
		self.sentence_break_of.pack(side=tk.LEFT, fill="y")
  
		self.given_substance = ttk.Combobox(self.user_input, values=self.equation.substances, width=15, state="readonly")
		self.given_substance.pack(side=tk.LEFT, padx=5, fill="y")

		self.sentence_break_to = ttk.Label(self.user_input, text="to", font=("Times New Roman", 20))
		self.sentence_break_to.pack(side=tk.LEFT, fill="y")
  
		self.wanted_measurement = ttk.Combobox(self.user_input, values=["g", "mol", "L", "r.p."], width=15, state="readonly")
		self.wanted_measurement.pack(side=tk.LEFT, padx=5, fill="y")
  
		self.sentence_break_of_duplicate = ttk.Label(self.user_input, text="of", font=("Times New Roman", 20))
		self.sentence_break_of_duplicate.pack(side=tk.LEFT, fill="y")
  
		self.wanted_substance = ttk.Combobox(self.user_input, values=self.equation.substances, width=15, state="readonly")
		self.wanted_substance.pack(side=tk.LEFT, padx=5, fill="y")
  
		self.submit.config(command=lambda: self.stoichiometry_inputs_checker())
  
	def stoichiometry_inputs_checker(self):
		"""
		Checks if the user inputted valid values for stoichiometry calculations.
		"""
		given_amount = self.given_amount.get()
		given_significant_figures = Significant_Figures().count([given_amount, 0], "*")[0]
		given_measurement = self.given_measurement.get()
		given_substance = self.given_substance.get()
		wanted_measurement = self.wanted_measurement.get()
		wanted_substance = self.wanted_substance.get()
  
		if given_measurement not in ["g", "mol", "L", "atoms / r.p."]:
			return messagebox.showerror("Given Measurement Check [4]", "The given measurement is not a valid measurement. Please select a valid measurement.")
  
		if given_substance not in self.equation.substances:
			return messagebox.showerror("Given Substance Check [5]", "The given substance is not a valid substance. Please select a valid substance.")
  
		if wanted_measurement not in ["g", "mol", "L", "atoms / r.p."]:
			return messagebox.showerror("Wanted Measurement Check [6]", "The wanted measurement is not a valid measurement. Please select a valid measurement.")
  
		if wanted_substance not in self.equation.substances:
			return messagebox.showerror("Wanted Substance Check [7]", "The wanted substance is not a valid substance. Please select a valid substance.")
  
		self.equation.stoichify(given_amount, given_significant_figures, given_measurement, given_substance, wanted_measurement, wanted_substance)

		for index, fraction in enumerate(self.equation.work_shown):
			if isinstance(fraction, str):
				label = tk.Label(self.work_shown_wrapper, text=fraction, font=("Times New Roman", 20))
				label.pack(side=tk.LEFT, padx=5)
			elif isinstance(fraction, tuple):
				self.create_fraction(self.work_shown_wrapper, fraction[0], fraction[1])
				if index+1 < len(self.equation.work_shown) and isinstance(self.equation.work_shown[index+1], tuple):
					label = tk.Label(self.work_shown_wrapper, text="×", font=("Times New Roman", 20))
					label.pack(side=tk.LEFT, padx=5) 

	def run(self):
		self.window.mainloop()

if __name__ == "__main__":
	# C3H8 + O2 → CO2 + H2O
	# 0238974C3H8 + 0239874O2 → 09248357CO2 + 824937H2O
	main_window = MainWindow()
	main_window.run()