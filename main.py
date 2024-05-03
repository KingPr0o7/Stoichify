import tkinter as tk # Framework for GUI (Probably Install?)
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
import re
import logic # Balancer
from logic import significant_figures_counter
import unicodedata
import sv_ttk # Custom theme for ttk (https://github.com/rdbende/Sun-Valley-ttk-theme - pip install sv-ttk)
from PIL import Image, ImageTk # Pillow image library (pip install pillow)

class MainWindow:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title("Stoichify")
		self.window.geometry("1600x900")
		sv_ttk.set_theme("dark")

		equation = tk.StringVar()

		self.navbar = ttk.Frame(self.window)
		self.navbar.pack(side="top", fill="x")

		self.user_input = ttk.Frame(self.window, height=10)
		self.user_input.pack(side="bottom", pady=15)

		self.equation_input = ttk.Entry(self.user_input, textvariable=equation, width=75)
		self.equation_input.pack(side="left", padx=15, fill="y")

		self.submit = ttk.Button(self.user_input, text="Submit", command=lambda: self.balance_equation(equation.get()))
		self.submit.config(style="Accent.TButton")
		self.submit.pack(side="right", fill="y")

	def replace_arrows(self, equation): #→⮕⇨🡒🡒⟶➜➔➝➞➨⭢🠂🠂🠊🠢🠦🠦🠮🠮🠒🠖🠚🠞🡢🡪🡲🡺
		"""
		Standardizes the arrow representation in the equation, removing any UNICODE arrow 
		and replacing it with '→'. The standard arrow for 'yields' in Chemistry.
		"""
		equation = ''.join(['→' if 'arrow' in unicodedata.name(char).lower() else char for char in equation])
		equation = equation.replace('->', '→')

		if '→' not in equation:
			return messagebox.showerror("'Yields' Arrow Check [0]", "The yields or any UNICODE arrow is not found in the equation. Please use '->' or '→' to represent the yields arrow, so the program can properly parse reactants and products.")		
  
		return equation

	def detect_substance_charges(self, equation):
		"""
		Finds if the user included substance charges in the equation, and rejects
		the equation if it does. Stoichify does not support charges in the equation, as 
		oxidation-reduction reactions require a different approach to balance.
		"""
		negative_charges = ['-', '−']

		plus_count = str(equation).count('+')
		delta = (len(self.substances) - 1) - plus_count
		if delta > 2:
			return messagebox.showerror("Equation Charges Check [1]", "Your equation includes charges (Oxidation-Reduction Reactions), which are not supported by Stoichify.")

		for substance in self.substances:
			if any(char in substance for char in negative_charges):
				return messagebox.showerror("Equation Charges Check [1]", "Your equation includes charges (Oxidation-Reduction Reactions), which are not supported by Stoichify.")

	def check_substance_concatenation(self, equation):
		"""
		Checks if the user properly concatenated substances in the equation using the '+' symbol.
		If not, the program will reject the equation and prompt the user to use '+' to separate substances,
		so the program can properly parse reactants and products.
		"""
		if '+' not in equation:
			return messagebox.showerror("Substance Concatenation '+' Check [2]", "The '+' symbol is not found in the equation. Please use '+' to separate substances in the equation.")

		for substance in self.substances:
			if len(substance) == 0:
				return messagebox.showerror("Substance Concatenation Length Check [3]", "There is an empty substance in the equation. Please remove the empty substance, and carefully type the equation again.")

	def remove_substance_states(self, equation):
		"""
		Removes all substance states in the equation, such as (s), (l), (g), and (aq).
		As the Stoichify does not need to know the state of the substance to balance the equation.
		"""
		substance_states = ['\([slgaq]*\)', '\([SLGAQ]*\)']
		for state in substance_states:
			equation = re.sub(state, "", equation)
		return equation

	def remove_coefficients(self, substance):
		"""
		Removes the coefficients from the substance.
		"""
		return re.sub(r'^\d+(?=[A-Z])', '', substance)
     

	def type_checking(self, equation):
		"""
		A series of checks to ensure the user inputted a valid chemical equation,
		that can be parsed and balanced by the Stoichify. If the equation passes all checks, the program
		will proceed into logic.py.
		"""
	
		type_checked_equation = self.replace_arrows(equation)
		self.reactants = str(type_checked_equation).replace(" ", "").split("→")[0].split("+")
		self.products = str(type_checked_equation).replace(" ", "").split("→")[1].split("+")
		self.reactants.append("→")
		self.substances = self.reactants + self.products
 
		self.detect_substance_charges(type_checked_equation)
		self.check_substance_concatenation(type_checked_equation)
		type_checked_equation = self.remove_substance_states(type_checked_equation)
		return type_checked_equation

	# def insert_subscripts(self, string):
	# 	"""
	# 	Inserts the subscript versions of integers provided in the string.
	# 	"""

	# 	subscript_digits = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
	# 	return string.translate(subscript_digits)

	def balance_equation(self, equation):
		"""
		Balances the chemical equation using the Stoichify algorithm.
		"""
		type_checked_equation = self.type_checking(equation)
		balanced_equation = logic.chemical_equation_balancer(type_checked_equation)
		self.reactants = str(balanced_equation).replace(" ", "").split("→")[0].split("+")
		self.products = str(balanced_equation).replace(" ", "").split("→")[1].split("+")
		# self.reactants.append("→")
		self.substances = self.reactants + self.products

		showing_chemical_equation = tk.Label(self.window, text=balanced_equation, font=("Times New Roman", 20))
		showing_chemical_equation.pack()

		self.equation_input.destroy()
		self.given_amount = ttk.Entry(self.user_input, width=10)
		self.given_amount.pack(side="left", fill="y")
  
		self.given_measurement = ttk.Combobox(self.user_input, values=["g", "mol", "L", "atoms / r.p."], width=15, state="readonly")
		self.given_measurement.pack(side="left", padx=5, fill="y")
  
		self.sentence_break_of = ttk.Label(self.user_input, text="of", font=("Times New Roman", 20))
		self.sentence_break_of.pack(side="left", fill="y")
  
		self.given_substance = ttk.Combobox(self.user_input, values=self.substances, width=15, state="readonly")
		self.given_substance.pack(side="left", padx=5, fill="y")

		self.sentence_break_to = ttk.Label(self.user_input, text="to", font=("Times New Roman", 20))
		self.sentence_break_to.pack(side="left", fill="y")
  
		self.wanted_measurement = ttk.Combobox(self.user_input, values=["g", "mol", "L", "atoms / r.p."], width=15, state="readonly")
		self.wanted_measurement.pack(side="left", padx=5, fill="y")
  
		self.sentence_break_of_duplicate = ttk.Label(self.user_input, text="of", font=("Times New Roman", 20))
		self.sentence_break_of_duplicate.pack(side="left", fill="y")
  
		self.wanted_substance = ttk.Combobox(self.user_input, values=self.substances, width=15, state="readonly")
		self.wanted_substance.pack(side="left", padx=5, fill="y")
  
		self.submit.config(command=lambda: self.stoichiometry_inputs_checker())
  
	def stoichiometry_inputs_checker(self):
		"""
		Checks if the user inputted valid values for stoichiometry calculations.
		"""
		given_amount = self.given_amount.get()
		print(significant_figures_counter([given_amount, 0], "*"))
		given_measurement = self.given_measurement.get()
		given_substance = self.given_substance.get()
		wanted_measurement = self.wanted_measurement.get()
		wanted_substance = self.wanted_substance.get()
  
		if not given_amount.isdigit():
			return messagebox.showerror("Given Amount Check [4]", "The given amount is not a valid number. Please input a valid number.")
  
		if given_measurement not in ["g", "mol", "L", "atoms / r.p."]:
			return messagebox.showerror("Given Measurement Check [5]", "The given measurement is not a valid measurement. Please select a valid measurement.")
  
		if given_substance not in self.substances:
			return messagebox.showerror("Given Substance Check [6]", "The given substance is not a valid substance. Please select a valid substance.")
  
		if wanted_measurement not in ["g", "mol", "L", "atoms / r.p."]:
			return messagebox.showerror("Wanted Measurement Check [7]", "The wanted measurement is not a valid measurement. Please select a valid measurement.")
  
		if wanted_substance not in self.substances:
			return messagebox.showerror("Wanted Substance Check [8]", "The wanted substance is not a valid substance. Please select a valid substance.")
  
		# self.stoichiometry_calculator(given_amount, given_measurement, given_substance, wanted_measurement, wanted_substance)

	def run(self):
		self.window.mainloop()

if __name__ == "__main__":
	# C3H8 + O2 → CO2 + H2O
	# 0238974C3H8 + 0239874O2 → 09248357CO2 + 824937H2O
	main_window = MainWindow()
	main_window.run()