import tkinter as tk # Framework for GUI (Probably Install?)
from tkinter import ttk
from tkinter import messagebox
import re
import logic # Balancer
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

		self.user_input = ttk.Frame(self.window)
		self.user_input.pack(side="bottom", pady=15)

		self.equation_input = ttk.Entry(self.user_input, textvariable=equation, width=75)
		self.equation_input.pack(side="left", padx=15)

		self.submit = ttk.Button(self.user_input, text="Submit", command=lambda: self.balance_equation(equation.get()))
		self.submit.pack(side="right")

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
		delta = (len(substances) - 1) - plus_count
		if delta > 2:
			return messagebox.showerror("Equation Charges Check [1]", "Your equation includes charges (Oxidation-Reduction Reactions), which are not supported by Stoichify.")

		for substance in substances:
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

		for substance in substances:
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

	def type_checking(self, equation):
		"""
		A series of checks to ensure the user inputted a valid chemical equation,
		that can be parsed and balanced by the Stoichify. If the equation passes all checks, the program
		will proceed into logic.py.
		"""
		global reactants, products, substances
	
		type_checked_equation = self.replace_arrows(equation)
		reactants = str(type_checked_equation).replace(" ", "").split("→")[0].split("+")
		products = str(type_checked_equation).replace(" ", "").split("→")[1].split("+")
		reactants.append("→")
		substances = reactants + products
	
		self.detect_substance_charges(type_checked_equation)
		self.check_substance_concatenation(type_checked_equation)
		type_checked_equation = self.remove_substance_states(type_checked_equation)
		return type_checked_equation

	def insert_subscripts(self, string):
		"""
		Inserts the subscript versions of integers provided in the string.
		"""

		subscript_digits = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
		return string.translate(subscript_digits)

	def balance_equation(self, equation):
		"""
		Balances the chemical equation using the Stoichify algorithm.
		"""
		type_checked_equation = self.type_checking(equation)
		balanced_coefficients = logic.chemical_equation_balancer(type_checked_equation)[0]

		pointer = 0
		balanced_equation = ""
 
		for index, substance in enumerate(substances):
			if substance != "→":
				if substance[0].isdigit():
					substance = substance[1:]
				self.insert_subscripts(substance)
				if index == len(substances) - 1:
					balanced_equation += f"{balanced_coefficients[pointer]}{substance}"
				else:
					if substances[index + 1] != "→":
						balanced_equation += f"{balanced_coefficients[pointer]}{substance} + "
					else:
						balanced_equation += f"{balanced_coefficients[pointer]}{substance} "
				pointer += 1
			else:
				balanced_equation += "→ "  

		showing_chemical_equation = tk.Label(self.window, text=balanced_equation, font=("Times New Roman", 20))
		showing_chemical_equation.pack()

		self.equation_input.destroy()
		self.substance_amount = ttk.Entry(self.user_input, width=10)
		self.substance_amount.pack(side="left")
  
		self.substance_measurement = ttk.Combobox(self.user_input, values=["g", "mol", "L", "atoms / r.p."], width=10, state="readonly")
		self.substance_measurement.pack(side="left", padx=5)
  
		self.substance_string_break = ttk.Label(self.user_input, text="of", font=("Times New Roman", 20))
		self.substance_string_break.pack(side="left")
  
		formatted_substances = []
  
		for substance in substances:
			substance = self.insert_subscripts(substance)
			if substance == "→":
				continue
			formatted_substances.append(substance)

		self.given_substance = ttk.Combobox(self.user_input, values=formatted_substances, width=10, state="readonly")
		self.given_substance.pack(side="left", padx=5)

	def run(self):
		self.window.mainloop()

if __name__ == "__main__":
	main_window = MainWindow()
	main_window.run()