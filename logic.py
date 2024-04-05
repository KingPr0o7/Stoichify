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

import re # Regular Expressions

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
	"reactants": {},
	"products": {}
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
					if index + 1 < len(substance) and str(substance[index + string_dilation]).isdigit(): # Check if next char is a number, while in range.
						element_subscript = substance_coefficient * int(substance[index + string_dilation]) * element_multiplier # Account for the coefficients, subscript, and parentheses (multipliers). 
						if DEBUG_MODE == True:
							if index + 1 < len(substance):
								print(f"{element}({element_subscript}) [Coefficient: {substance_coefficient} * Subscript: {str(substance[index + string_dilation])} * Multiplier: {element_multiplier}]")
					else: # If not a number, the subscript is 1.
						if DEBUG_MODE == True:
							print(f"{element}({element_subscript}) [Coefficient: {substance_coefficient} * Subscript: {element_subscript} * Multiplier: {element_multiplier}]")
						element_subscript = substance_coefficient * element_subscript * element_multiplier # Account for the coefficients, subscript (1), and parentheses (multipliers).
					chemical_equation[f"{side}"][element] = element_subscript  

def chemical_equation_balancer(equation):
	chemical_equation["string"] = str(equation)

	reactants = chemical_equation["string"].replace(" ", "").split("->")[0].split("+")
	products = chemical_equation["string"].replace(" ", "").split("->")[1].split("+")
	print(f"Reactants: {reactants}", "->", f"Products: {products}", "\n")

	substance_scanner("reactants", reactants)
	substance_scanner("products", products)


chemical_equation_balancer("2AgI + 2Fe2(CO3)3 -> FeI3 + Ag2CO3")
print(f"Reactant Substances: {chemical_equation['reactants']}")
print(f"Product Substances: {chemical_equation['products']}")