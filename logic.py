#
# Outline
#   1. Categorize and split the chemical equation
#	2. Gather stoichiometric coefficients
# 	3. Balance the chemical equation
# 	4. Apply Mole Ratios
# 	5. Other (LR, Y)
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

STP = 22.4 # Standard Temperature and Pressure (L/mol)
AVOGADRO = 6.022 * 10**23 # Avogadro's number (particles/mol)
ALPHABET = "^[a-zA-Z]$"

#
# Formula Chemical Equation
#   Gather, split, and balance the user's chemical equation.
#

chemical_equation = {
	"string": "",
	"reactants": {},
	"products": {}
}

def element_finder(index, pointer, char, substance):
	element = ""
	if str(substance[index + 1]).islower():
		element = f"{char}{substance[index + 1]}"
		pointer += 2
	else:
		if re.match(ALPHABET, char):
			print(element)
			pointer += 1  
	element = substance[pointer]
	return pointer, element
       
def substance_collector(side, substance_list):
	for substance in substance_list:
		element_coefficient = substance[0]
	
		if re.match(ALPHABET, element_coefficient):
			element_coefficient = 1

		pointer = 0

		for index, char in enumerate(substance): 
			if pointer >= len(substance):
				break
			
			if substance[pointer] != "(":
				pointer, element = element_finder(index, pointer, char, substance)
			elif substance[pointer] == ")":
				pointer = len(substance)
			else:
				pointer += 1
				pointer, element = element_finder(index, pointer, char, substance)
				element_multiplier = int(substance[-1])
   
			# if pointer < len(substance):
			# 	print(substance[pointer])
   
			element_subscript = 1
			if pointer < len(substance) - 1 and str(substance[pointer]).isdigit():
				element_subscript = substance[pointer]
				pointer += 1
			# print(f"{element}({element_subscript})")
    
			# 	element_amount = int(element_coefficient) * int(element_subscript)
			# 	# print(f"[{element_coefficient}]{element}({element_subscript}) = {element_amount}")
			# 	chemical_equation[f"{side}"][element] = element_amount   

def chemical_equation_balancer(equation):
	chemical_equation["string"] = str(equation)
	# print(chemical_equation["string"].split(" "))

	reactants = chemical_equation["string"].replace(" ", "").split("->")[0].split("+")
	products = chemical_equation["string"].replace(" ", "").split("->")[1].split("+")
	print(f"Reactants: {reactants}", "->", f"Products: {products}", "\n")

	substance_collector("reactants", reactants)
	substance_collector("products", products)


chemical_equation_balancer("AgI + Fe2(CO3)3 -> FeI3 + Ag2CO3")
print(f"Reactant Substances: {chemical_equation['reactants']}")
print(f"Product Substances: {chemical_equation['products']}")