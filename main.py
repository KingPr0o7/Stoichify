import tkinter as tk # Framework for GUI (Probably Install?)
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
import re
import entities # Balancer
from entities import Equation
from sig_figs import Significant_Figures
import unicodedata
import sv_ttk # Custom theme for ttk (https://github.com/rdbende/Sun-Valley-ttk-theme - pip install sv-ttk)
from PIL import Image, ImageTk # Pillow image library (pip install pillow)

class MainWindow:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("Stoichify")
		self.window.geometry("1000x500")
		
		self.substances = []
		# ---------------
		sv_ttk.set_theme("dark")

		self.equation = tk.StringVar()

		self.navbar = ttk.Frame(self.window)
		self.navbar.pack(side="top", fill="x")

		self.user_input = ttk.Frame(self.window, height=10)
		self.user_input.pack(side="bottom", pady=15)

		self.equation_input = ttk.Entry(self.user_input, textvariable=self.equation, width=75)
		self.equation_input.pack(side="left", padx=15, fill="y")

		self.submit = ttk.Button(self.user_input, text="Submit", command=lambda: self.balance_equation(self.equation.get()))
		self.submit.config(style="Accent.TButton")
		self.submit.pack(side="right", fill="y")

	def create_fraction(self, frame, numerator_text, denominator_text): 
		fraction_holder = tk.Frame(frame)
		fraction_holder.pack(side=tk.LEFT, padx=5)
     
		max_length = max(len(numerator_text), len(denominator_text))
	
		numerator = tk.Label(fraction_holder, text=numerator_text, font=("Times New Roman", 20), width=max_length)
		numerator.pack(side=tk.TOP)
	
		line = tk.Frame(fraction_holder, height=1, width=200, bg="white")
		line.pack(side=tk.TOP, fill=tk.X)
	
		denominator = tk.Label(fraction_holder, text=denominator_text, font=("Times New Roman", 20), width=max_length)
		denominator.pack(side=tk.TOP)

	def balance_equation(self, equation):
		"""
		Balances the chemical equation using the Stoichify algorithm.
		"""
		self.equation = Equation(equation)

		showing_chemical_equation = tk.Label(self.window, text=self.equation.balanced, font=("Times New Roman", 20))
		showing_chemical_equation.pack()

		self.work_shown_wrapper = tk.Frame(self.window)
		self.work_shown_wrapper.pack(fill="x", pady=15, anchor="center")

		self.equation_input.destroy()
		self.given_amount = ttk.Entry(self.user_input, width=25)
		self.given_amount.pack(side="left", fill="y")
  
		self.given_measurement = ttk.Combobox(self.user_input, values=["g", "mol", "L", "r.p."], width=15, state="readonly")
		self.given_measurement.pack(side="left", padx=5, fill="y")
  
		self.sentence_break_of = ttk.Label(self.user_input, text="of", font=("Times New Roman", 20))
		self.sentence_break_of.pack(side="left", fill="y")
  
		self.given_substance = ttk.Combobox(self.user_input, values=self.equation.substances, width=15, state="readonly")
		self.given_substance.pack(side="left", padx=5, fill="y")

		self.sentence_break_to = ttk.Label(self.user_input, text="to", font=("Times New Roman", 20))
		self.sentence_break_to.pack(side="left", fill="y")
  
		self.wanted_measurement = ttk.Combobox(self.user_input, values=["g", "mol", "L", "r.p."], width=15, state="readonly")
		self.wanted_measurement.pack(side="left", padx=5, fill="y")
  
		self.sentence_break_of_duplicate = ttk.Label(self.user_input, text="of", font=("Times New Roman", 20))
		self.sentence_break_of_duplicate.pack(side="left", fill="y")
  
		self.wanted_substance = ttk.Combobox(self.user_input, values=self.equation.substances, width=15, state="readonly")
		self.wanted_substance.pack(side="left", padx=5, fill="y")
  
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