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

#
# Constants
#   Required scientific numbers used to bridge needed calculations.
#

DEBUG_MODE = False # Toggle to True to see the properties of the chemical equation 
STP = 22.4 # Standard Temperature and Pressure (L/mol)
AVOGADRO = 6.022 * 10**23 # Avogadro's number (particles/mol)
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
			
    
def substance_scanner(side, substance_list):
	"""
    Loops through one side (reactants or products) of a chemical equation,
    checking each substance's coefficient (always placed at the 0th index). 
    Then, loops within such side (a substance) to perform element scans and
    subscript calculations to be added the chemical_equation dictionary. 
    """
	for substance in substance_list:
		substance_coefficient = substance[0] # Get the coefficient at the 0th index
		element_multiplier = 1 # If parentheses aren't detected, the subscript is 1 by default
     
		if re.match(UPPERCASE, substance_coefficient): # When not provided, a substance has a coefficient of 1
			substance_coefficient = 1	
		elif str(substance_coefficient).isdigit(): # When provided
			substance_coefficient = int(substance[0])
	
		chemical_equation[side][substance] = [] # Create a list for each substance in the side
 
		for index, char in enumerate(substance):
			element_subscript = 1 # Same as coefficients; if not provided; it's 1.
			string_dilation = 1 # Used to traverse the string

			if char == "(": # If a set of parentheses is detected, it has to have a subscript (multiplier)  
				if substance[-1] == "]": # If the last character is a closing bracket, the subscript is the second to last character (the reactant is then a complex ion)
					element_multiplier = int(substance[-2])
				else:			
					element_multiplier = int(substance[-1])
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
					chemical_equation[side][substance].append((element, element_data))

def matrix_builder(side):
	"""
	Creates a matrix of each element's amount (subscript * multiplier) in each substance of the side
	(reactants or products (-1 to distinguish between the two)). 
	"""
	for substance in chemical_equation[side]:
		matrix_row = []
		for element in chemical_equation["elements"]:
			found = False
			for substance_element in chemical_equation[side][substance]:
				if substance_element[0] == element:
					if side == "reactants":
						matrix_row.append(substance_element[1][1] * substance_element[1][2])
					else:
						matrix_row.append(substance_element[1][1] * substance_element[1][2] * -1) # Exclude negatives + designate products
					found = True
					break
			if not found:
				matrix_row.append(0)
		chemical_equation["element_matrix"].append(matrix_row)    

def chemical_equation_balancer(equation):
	"""
	Splits reactants and products, scans for elements, builds a matrix, solves the matrix, 
	balances the chemical equation, and saves results as a valid chemical equation. Balancing logic 
	wouldn't be possible without the use of matrices and linear algebra by Mohammad-Ali Bandzar -
	(https://medium.com/swlh/balancing-chemical-equations-with-python-837518c9075b).
	"""
	chemical_equation["unbalanced"] = str(equation)

	reactants = chemical_equation["unbalanced"].replace(" ", "").split("->")[0].split("+")
	products = chemical_equation["unbalanced"].replace(" ", "").split("->")[1].split("+")

	if DEBUG_MODE == True:
		print(f"\nReactants: {reactants}", "->", f"Products: {products}", "\n")

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

	reactants.append("->")
	substances = reactants + products
	pointer = 0

	for_show_balanced = ""
 
	for index, substance in enumerate(substances):
		if substance != "->":
			if substance[0].isdigit():
				substance = substance[1:]
			if index == len(substances) - 1:
				chemical_equation["balanced"] += f"{balanced_coefficients[pointer]}{substance}"
				for_show_balanced += f"\033[1m{balanced_coefficients[pointer]}\033[0m{substance}"
			else:
				if substances[index + 1] != "->":
					chemical_equation["balanced"] += f"{balanced_coefficients[pointer]}{substance} + "
					for_show_balanced += f"\033[1m{balanced_coefficients[pointer]}\033[0m{substance} + "
				else:
					chemical_equation["balanced"] += f"{balanced_coefficients[pointer]}{substance} "
					for_show_balanced += f"\033[1m{balanced_coefficients[pointer]}\033[0m{substance} "
			pointer += 1
		else:
			chemical_equation["balanced"] += "-> " 
			for_show_balanced += "-> "

	if DEBUG_MODE == True:
		print(f"\nUnbalanced Chemical Equation: {chemical_equation['unbalanced']}")
	print(f"Balanced Chemical Equation: {for_show_balanced}")

#
# Examples of Unbalanced Chemical Equations
#
# AgI + Fe2(CO3)3 -> FeI3 + Ag2CO3 
# KMnO4 + HCl -> MnCl2 + KCl + Cl2 + H2O
# Al + O2 -> Al2O3
# C2H4 + O2 -> CO2 + H2O
# Ca3(PO4)2 + SiO2 + C -> CaSiO3 + P4 + CO
# NH3 + O2 -> NO + H2O
# NaOH + H2S04 -> Na2S04 + H20
# Ca(OH)2 + H3PO4 -> Ca3(PO4)2 + H2O
# K4[Fe(SCN)6] + K2Cr2O7 + H2SO4 -> Fe2(SO4)3 + Cr2(SO4)3 + CO2 + H2O + K2SO4 + KNO3 (Hardest I could find)
# Zn + HNO3 -> Zn(NO3)2 + H2O + N2O

if __name__ == "__main__":
	if DEBUG_MODE == True:
		chemical_equation_balancer("K4[Fe(SCN)6] + K2Cr2O7 + H2SO4 -> Fe2(SO4)3 + Cr2(SO4)3 + CO2 + H2O + K2SO4 + KNO3") # Insert your chemical equation here
		print(f"\nReactant Substances: {chemical_equation['reactants']}")
		print(f"Product Substances: {chemical_equation['products']}") 
	else:
		user_chemical_equation = input("Enter a chemical equation: ")
		chemical_equation_balancer(user_chemical_equation)