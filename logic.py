#
# Nathan Parker | 4/11/24 | v0.3.0
# A CLI based chemical equation balancer that can balance any chemical equation.
# Done by collecting subscripts, coefficients, and multipliers from the string (the chemical equation),
# and to be calculated for their amounts, and processed into a matrix to be solved by linear algebra.
#
# DOCUMENTATION COMING SOON. (I need to finish the other logic/steps first.)
# 	For the time being, please refer to line comments and header comments 
# 	for an understanding of the code.
#

#
# Outline
#   1. Categorize and split the chemical equation [DONE]
#	2. Gather stoichiometric coefficients [DONE]
# 	3. Balance the chemical equation [DONE]
# 	4. Apply Mole Ratios
# 	5. Other (Limiting Reactant, Percent (%) Yield)
#	6. Error Detection
#	7. User Interface
#	8. Show Steps 
#

#
# Imports
#   Libraries or modules that are required and used
#   in this module.
#

import re # Regular Expressions (String Checking)
import sympy # Symbolic Mathematics (Equations)
from sympy import Matrix, lcm # Matrix Operations, Least Common Multiple
import math # Mathematics (Rounding)
from chemlib import Element # Chemical Library (Molar Masses)
#
# Constants
#   Required scientific numbers used to bridge needed calculations.
#

DEBUG_MODE = False # Toggle to True to see the properties of the chemical equation 
STP = 22.4 # Standard Temperature and Pressure (L/mol)
AVOGADRO = 6.02214 * 10**23 # Avogadro's number (particles/mol)]
UPPERCASE = "^[A-Z]$"
LOWERCASE = "^[a-z]$"

#
# Formula Chemical Equation
#   Gather, split, and balance the user's chemical equation.
#

chemical_equation = {
	"unbalanced": "", # User's inputted chemical equation
	"elements": [], # All elements (uniques) within the chemical equation
	"reactants": {}, # Reactants and their elements
	"products": {}, # Products and their elements
	"element_matrix": [], # Amounts of each substance into a matrix
	"balanced": "" # Balanced chemical equation
}

def element_scanner(index, substance):
	"""
	Takes a string (AKA a substance) and first scans for a capital character.
	Upon finding a capital letter, it checks the next character's capitalization state 
	to see if it's a two-lettered element. If the second character isn't a lowercase 
	character it's a single element. 
	"""
	element = "-"
	if index <= len(substance): # Ensure within range
		if re.match(UPPERCASE, substance[index]):
			element = substance[index] # Assume it's a single-lettered element
			if index + 1 < len(substance) and re.match(LOWERCASE, substance[index + 1]): # Check the next character's capitalization state (keeping in range)
				element = f"{substance[index]}{substance[index + 1]}"
	# Add element to the list of elements to build the matrix
	if element != "-" and element not in chemical_equation["elements"]:
		chemical_equation["elements"].append(element)
	return element
			
	
def substance_scanner(side, substance_list, mode="iteration"):
	"""
	Loops through one side (reactants or products) of a chemical equation,
	setting each substance's coefficient to 1 (they aren't needed). 
	Then, loops within such side (a substance) to perform element scans and
	subscript calculations to be added the chemical_equation dictionary. 
	"""
	for substance in substance_list:
		substance_coefficient = 1
		element_multiplier = 1 # If parentheses aren't detected, the subscript is 1 by default
 
		if mode == "iteration":
			chemical_equation[side][substance] = [] # Create a list for each substance in the side
		elif mode == "inspection":
			substance_elemental_makeup = []
 
		for index, char in enumerate(substance):
			element_subscript = 1 # Same as coefficients; if not provided; it's 1.
			string_dilation = 1 # Used to traverse the string

			if char == "(":
				closing_parenthesis_index = str(substance).index(")")
				element_multiplier = int(substance[closing_parenthesis_index + 1])
				continue
			elif char == ")":
				element_multiplier = 1 # Reset the multiplier
				continue
			elif char == "[" or char == "]": # If a closing bracket is detected, it's a complex ion
				continue
			elif char != "(" and char != ")":
				element = element_scanner(index, substance)
				if element == "-": # Ignore elements that aren't found (trust me bro, the scanner works (at least I hope))
					continue
				else:
					if len(element) == 2: # Move pointer over 2, to get to the end of the two-lettered elements
						string_dilation = 2
						if string_dilation + index > len(substance) - 1: # Ensure range
							string_dilation = 1
					if index + 1 < len(substance) and str(substance[index + string_dilation]).isdigit(): # Check if next char is a number, while in range.
						# Account for multiple digit subscripts (e.g. C6H12O6, C12H22O11, etc.)
						subscripts = ""
						subscript_index = index + string_dilation
						while subscript_index < len(substance) and str(substance[subscript_index]).isdigit(): # Loop through as long as the next character is a number
							subscripts += substance[subscript_index]
							subscript_index += 1
						element_subscript = int(subscripts)
					else: # If not a number, the subscript is 1.
						element_subscript = element_subscript
					element_data = (substance_coefficient, element_subscript, element_multiplier)
					if mode == "iteration":
						chemical_equation[side][substance].append((element, element_data))
					elif mode == "inspection":
						substance_elemental_makeup.append((element, element_data))
		if mode == "inspection":
			return substance_elemental_makeup

def matrix_builder(side):
	"""
	Creates a matrix of each element's amount (subscript * multiplier) in each substance of the side
	(reactants or products (-1 to distinguish between the two)). 
	"""
	for substance in chemical_equation[side]:
		matrix_row = []
		for element in chemical_equation["elements"]:
			element_total = 0
			for substance_element in chemical_equation[side][substance]:
				if substance_element[0] == element:
					if side == "reactants":
						element_total += substance_element[1][1] * substance_element[1][2]
					else:
						element_total += substance_element[1][1] * substance_element[1][2] * -1 # Exclude negatives + designate products
			matrix_row.append(element_total)
		chemical_equation["element_matrix"].append(matrix_row)

def chemical_equation_balancer(equation):
	"""
	Splits reactants and products, scans for elements, builds a matrix, solves the matrix, 
	balances the chemical equation, and saves results as a valid chemical equation. Balancing logic 
	wouldn't be possible without the use of matrices and linear algebra by Mohammad-Ali Bandzar -
	(https://medium.com/swlh/balancing-chemical-equations-with-python-837518c9075b).
	"""
	chemical_equation["unbalanced"] = str(equation)

	reactants = chemical_equation["unbalanced"].replace(" ", "").split("→")[0].split("+")
	products = chemical_equation["unbalanced"].replace(" ", "").split("→")[1].split("+")

	if DEBUG_MODE == True:
		print(f"\nReactants: {reactants}", "→", f"Products: {products}", "\n")

	substance_scanner("reactants", reactants)
	substance_scanner("products", products)

	if DEBUG_MODE == True:
		print(f"All Elements Present: {chemical_equation['elements']} ({len(chemical_equation['elements'])})\n")

	matrix_builder("reactants")
	matrix_builder("products")	  

	# Use smypy to solve the matrix via linear algebra (Thanks to Mohammad-Ali Bandzar for this logic/code)
	matrix = Matrix(chemical_equation["element_matrix"])
	matrix = matrix.transpose() # Swap the rows and columns
	solution = matrix.nullspace()[0] # Solve the matrix
	multiple = lcm([val.q for val in solution]) # Find the least common multiple (LCM) of the denominators 
	balanced_coefficients = multiple * solution # Multiply by LCM to remove fractions (either solution is valid)

	if DEBUG_MODE == True:
		print(f"Chemical Matrix: {chemical_equation['element_matrix']} = {balanced_coefficients}\n")

	reactants.append("→")
	substances = reactants + products
	pointer = 0

	for_show_balanced = ""
 
	for index, substance in enumerate(substances):
		if substance != "→":
			substance = re.sub(r'^\d+(?=[A-Z])', '', substance)
			subscript_digits = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
			substance = substance.translate(subscript_digits)
			if index == len(substances) - 1:
				chemical_equation["balanced"] += f"{balanced_coefficients[pointer]}{substance}"
				for_show_balanced += f"\033[1m{balanced_coefficients[pointer]}\033[0m{substance}"
			else:
				if substances[index + 1] != "→":
					chemical_equation["balanced"] += f"{balanced_coefficients[pointer]}{substance} + "
					for_show_balanced += f"\033[1m{balanced_coefficients[pointer]}\033[0m{substance} + "
				else:
					chemical_equation["balanced"] += f"{balanced_coefficients[pointer]}{substance} "
					for_show_balanced += f"\033[1m{balanced_coefficients[pointer]}\033[0m{substance} "
			pointer += 1
		else:
			chemical_equation["balanced"] += "→ " 
			for_show_balanced += "→ "

	if DEBUG_MODE == True:
		print(f"\nUnbalanced Chemical Equation: {chemical_equation['unbalanced']}")
	return chemical_equation["balanced"]

def substance_coefficient(substance):
	"""
	"""
	coefficient_match = re.match(r"(\d+)[A-Z]", substance)
	coefficient = 1
	if coefficient_match:
		coefficient = int(coefficient_match.group(1))
	return coefficient

def significant_figures_counter(figures: list, mode):
	"""
	"""
	significant_figures = []
	if isinstance(figures[0], str):
		if mode == "*":
			if "." in figures[0]:
				figure = figures[0].replace(".", "")
				zeros_removed = figure.lstrip("0")
			else:
				zeros_removed = figures[0].lstrip("0").rstrip("0")
			significant_figures = len(zeros_removed)
			return significant_figures, figures[0]
	else:
		for figure in figures:
				if "." in str(figure):
					if mode == "+":
						significant_figures.append(len(str(figure).split(".")[1]))
					elif mode == "*":
						figure = str(figure).replace(".", "")
						zeros_removed = figure.lstrip("0").rstrip("0")
						significant_figures.append(len(zeros_removed))
				else:
					if mode == "+":
						significant_figures.append(0)
	if mode == "+":
		significant_figures = min(significant_figures)
	return significant_figures

def significant_figure_rounder(num, sig_figs):
	"""
	https://stackoverflow.com/a/3411435/20617039
	"""
	if num != 0:
		result = round(num, -int(math.floor(math.log10(abs(num))) + (1 - sig_figs)))
		if sig_figs <= math.floor(math.log10(abs(num))) + 1:
			return int(result)
		else:
			return result
	else:
		return 0  # Can't take the log of 0

def measurement_converter(amount, measurement, substance, type):
	significant_figures = 0
    
	if measurement == "L":
		amount = amount * STP if type == "*" else amount / STP if type == "/" else amount
		significant_figures = 3
	elif measurement == "atoms / r.p.":
		amount = amount * AVOGADRO if type == "*" else amount / AVOGADRO if type == "/" else amount
		significant_figures = 6
	elif measurement == "g":
		elemental_makeup = substance_scanner("-", [substance], "inspection")
		molar_masses = []
		molar_mass = 0

		for element in elemental_makeup:
			atomic_mass = Element(element[0]).properties['AtomicMass']
			molar_masses.append(atomic_mass)
			molar_mass += atomic_mass * element[1][1]

		print(f"Molar Masses: {molar_masses}")

		significant_figures = significant_figures_counter(molar_masses, "+")
		print(f"Significant Figures: {significant_figures} ({molar_masses})")

		molar_mass = round(molar_mass, significant_figures)
		print(f"Molar Mass: {molar_mass}")
		amount = amount * molar_mass if type == "*" else amount / molar_mass if type == "/" else amount

	return amount, significant_figures

def stoichify(given_amount, given_significant_figures, given_measurement, given_substance, wanted_measurement, wanted_substance):
	"""
	"""
	answer = 0
	current_measurement = given_measurement
	significant_figures = []
	significant_figures.append(given_significant_figures)

	if current_measurement != "mol":
		given_amount, conversion_significant_figures = measurement_converter(given_amount, given_measurement, given_substance, "/")
		current_measurement = "mol"
		significant_figures.append(conversion_significant_figures)
  
	# Molar Bridge
	wanted_coefficient = substance_coefficient(wanted_substance)
	given_coefficient = substance_coefficient(given_substance)
	answer = given_amount * (wanted_coefficient / given_coefficient)
	significant_figures.append(float('inf'))
	significant_figures.append(float('inf'))

	if wanted_measurement != "mol":
		answer, conversion_significant_figures = measurement_converter(answer, wanted_measurement, wanted_substance, "*")
		significant_figures.append(conversion_significant_figures)
 
	print(f"Significant Figures: {significant_figures} (Lowest: {min(significant_figures)})\nAnswer: {answer}")
 
	answer = significant_figure_rounder(answer, min(significant_figures))

	return f"{answer} {wanted_measurement} {wanted_substance}"
		

# if decimal_places == 0:
# 	return int(number + 0.5)
# else: 
# 	value = 10 ** decimal_places
# 	return int(number * value + 0.5) / value 
#
# Examples of Unbalanced Chemical Equations
#
# AgI + Fe2(CO3)3 → FeI3 + Ag2CO3 
# KMnO4 + HCl → MnCl2 + KCl + Cl2 + H2O
# Al + O2 → Al2O3
# C2H4 + O2 → CO2 + H2O
# Ca3(PO4)2 + SiO2 + C → CaSiO3 + P4 + CO
# NH3 + O2 → NO + H2O
# NaOH + H2S04 → Na2S04 + H20
# Ca(OH)2 + H3PO4 → Ca3(PO4)2 + H2O
# K4[Fe(SCN)6] + K2Cr2O7 + H2SO4 → Fe2(SO4)3 + Cr2(SO4)3 + CO2 + H2O + K2SO4 + KNO3 (Hardest I could find)
# Zn + HNO3 → Zn(NO3)2 + H2O + N2O
# H2(g) + O2(g) → H2O(l)

if __name__ == "__main__":
	if DEBUG_MODE == True:
		print(chemical_equation_balancer("K4[Fe(SCN)6] + K2Cr2O7 + H2SO4 → Fe2(SO4)3 + Cr2(SO4)3 + CO2 + H2O + K2SO4 + KNO3")) # Insert your chemical equation here
		print(f"\nReactant Substances: {chemical_equation['reactants']}")
		print(f"Product Substances: {chemical_equation['products']}") 
	else:
		# print(chemical_equation_balancer("C3H8 + O2 → CO2 + H2O"))
		# print(stoichify(2.8, 2, "mol", "1C3H8", "g", "3CO2")) # Insert your stoichiometry here
  
		# print(chemical_equation_balancer("SO2 + O2 → SO3"))
		# print(stoichify(3.4, 2, "mol", "2SO2", "mol", "2SO3"))

		# print(chemical_equation_balancer("SO2 + O2 → SO3"))
		# print(stoichify(4.7, 2, "mol", "2SO2", "mol", "1O2"))
  
		# print(chemical_equation_balancer("C3H8 + O2 → CO2 + H2O"))
		# print(stoichify(25, 2, "g", "1C3H8", "mol", "4H2O"))
  
		# print(chemical_equation_balancer("C3H8 + O2 → CO2 + H2O"))
		# print(stoichify(38, 2, "g", "4H2O", "mol", "3CO2"))		

		# print(chemical_equation_balancer("Al + Cl2 → AlCl3"))
		# print(stoichify(35, 2, "g", "2Al", "g", "2AlCl3"))

		print(chemical_equation_balancer("Al + Cl2 → AlCl3"))
		print(stoichify(42.8, 3, "g", "2Al", "g", "3Cl2"))

		# user_chemical_equation = input("Enter a chemical equation: ")
		# print(chemical_equation_balancer(user_chemical_equation))