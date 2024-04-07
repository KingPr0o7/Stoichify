#
# Outline
#   1. Categorize and split the chemical equation [DONE]
#	2. Gather stoichiometric coefficients [DONE]
# 	3. Balance the chemical equation
# 	4. Apply Mole Ratios
# 	5. Other (Limiting Reactant, Percent (%) Yield)
#	6. Error Detection
#

#
# Imports
#   Libaries or modules that are required and used
#   in this module.
#

import re # Regular Expressions (String Checking)
import fractions # Fraction Utils (Finding the Greatest Common Denominator (GCD))

#
# Constants
#   Required scientific numbers used to bridge needed calculations.
#

DEBUG_MODE = True
STP = 22.4 # Standard Temperature and Pressure (L/mol)
AVOGADRO = 6.022 * 10**23 # Avogadro's number (particles/mol)
UPPERCASE = "^[A-Z]$"
LOWERCASE = "^[a-z]$"

#
# Formula Chemical Equation
#   Gather, split, and balance the user's chemical equation.
#

chemical_equation = {
	"string": "",
	"reactants": [],
	"products": []
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
	return element
			
    
def substance_scanner(side, substance_list):
	"""
    Loops through one side (reactants or products) of a chemical equation,
    checking each substance's coefficient (always placed at the 0th index). 
    Then, loops within such side (a substance) to perform element scans and
    subscript calculations to be added the chemical_equation dictionary. 
    """
	for substance in substance_list:
		# Make variables not local
		substance_coefficient = substance[0] # Get the coefficient at the 0th index
		element_multiplier = 1
     
		if re.match(UPPERCASE, substance_coefficient): # When not provided, a substance has a coefficient of 1.
			substance_coefficient = 1	
		elif str(substance_coefficient).isdigit(): # When provided
			substance_coefficient = int(substance[0])
	
		for index, char in enumerate(substance):
			# Make variables not local
			element_subscript = 1 # Same as coefficients; if not provided; it's one.
			string_dilation = 1 # Used to traverse the string
	
			if char == "(": # If a set of parentheses is detected, it has to have a subscript (multiplier)  
				element_multiplier = int(substance[-1])
				continue 
			elif char != "(" and char != ")":
				element = element_scanner(index, substance)
				if element == "-": # Ignore elements that aren't found (trust me bro, the scanner works (at least I hope))
					continue
				else:
					if len(element) == 2: # Move pointer over 2, to get to the end of the two-lettered elements
						string_dilation = 2
						if string_dilation + index > len(substance) - 1:
							string_dilation = 1
					if index + 1 < len(substance) and str(substance[index + string_dilation]).isdigit(): # Check if next char is a number, while in range.
						element_subscript = int(substance[index + string_dilation])
					else: # If not a number, the subscript is 1.
						element_subscript = element_subscript
					# print(element, substance_coefficient, element_subscript, element_multiplier)
					element_data = (substance_coefficient, element_subscript, element_multiplier)
					chemical_equation[side].append((element, element_data))

def chemical_equation_balancer(equation):
	chemical_equation["string"] = str(equation)

	reactants = chemical_equation["string"].replace(" ", "").split("->")[0].split("+")
	products = chemical_equation["string"].replace(" ", "").split("->")[1].split("+")
	print(f"Reactants: {reactants}", "->", f"Products: {products}", "\n")

	substance_scanner("reactants", reactants)
	substance_scanner("products", products)

	variables = {}
 
	for reactant_element in chemical_equation['reactants']:
		reactant_element_amount = reactant_element[1][1] * reactant_element[1][2]
		if reactant_element[0] not in variables:
			variables[reactant_element[0]] = [reactant_element_amount]
		else:
			variables[reactant_element[0]].append(reactant_element_amount)
 
	for product_element in chemical_equation['products']:
		product_element_amount = product_element[1][1] * product_element[1][2]
		if product_element[0] not in variables:
			variables[product_element[0]] = [product_element_amount]
		else:
			variables[product_element[0]].append(product_element_amount)  

	known_variable = 1 # The known variable (usually referred to as a) is always going to be 1, to start the chain reactions (pun intended) to solve the unknowns.

# for var in variables:
# 	fraction = fractions.Fraction(var).limit_denominator()
	# print(var, fraction)

	print(variables)

     
chemical_equation_balancer("Ca3(PO4)2 + SiO2 + C -> CaSiO3 + P4 + CO") # AgI + Fe2(CO3)3 -> FeI3 + Ag2CO3 | KMnO4 + HCl -> MnCl2 + KCl + Cl2 + H2O | Al + O2 -> Al2O3 | C2H4 + O2 -> CO2 + H2O
print(f"Reactant Substances: {chemical_equation['reactants']}")
print(f"Product Substances: {chemical_equation['products']}")