import os
import re
from prettytable import PrettyTable
from prettytable import SINGLE_BORDER
from prettytable import DOUBLE_BORDER

# Used for clearing the console. (Replit uses Linux) 
system = 'Linux'

def clear_console(system):
	if str(system).lower() == 'windows' or str(system).lower() == 'win':
		os.system('cls')
	elif str(system).lower() == 'linux':
		os.system('clear')

clear_console(system)

# String Formatter (Colors & Display Style)
class str_format:
	# Single
	PASS = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	# Combinations
	BOLD_UNDERLINE = '\033[1m\033[4m'
	PASS_BOLD = '\033[92m\033[1m'
	PASS_UNDERLINE = '\033[92m\033[4m'
	PASS_BOLD_UNDERLINE = '\033[92m\033[1m\033[4m'
	WARNING_BOLD = '\033[93m\033[1m'
	WARNING_UNDERLINE = '\033[93m\033[4m'
	WARNING_BOLD_UNDERLINE = '\033[93m\033[1m\033[4m'
	FAIL_BOLD = '\033[91m\033[1m'
	FAIL_UNDERLINE = '\033[91m\033[4m'
	FAIL_BOLD_UNDERLINE = '\033[91m\033[1m\033[4m'
	# End
	END = '\033[0m'

def format_str(style, text):
	style_map = {
	# Single
	'PASS': str_format.PASS,
	'WARNING': str_format.WARNING,
	'FAIL': str_format.FAIL,
	'BOLD': str_format.BOLD,
	'UNDERLINE': str_format.UNDERLINE,
	# Combinations 
	'BOLD_UNDERLINE': str_format.BOLD_UNDERLINE,
	'PASS_BOLD': str_format.PASS_BOLD,
	'PASS_UNDERLINE': str_format.PASS_UNDERLINE,
	'PASS_BOLD_UNDERLINE': str_format.PASS_BOLD_UNDERLINE,
	'WARNING_BOLD': str_format.WARNING_BOLD,
	'WARNING_UNDERLINE': str_format.WARNING_UNDERLINE,
	'WARNING_BOLD_UNDERLINE': str_format.WARNING_BOLD_UNDERLINE,
	'FAIL_BOLD': str_format.FAIL_BOLD,
	'FAIL_UNDERLINE': str_format.FAIL_UNDERLINE,
	'FAIL_BOLD_UNDERLINE': str_format.FAIL_BOLD_UNDERLINE,
	'END': str_format.END
	}
	return f'{style_map.get(style, "") + text + str_format.END}'

# --------------------------------------------------------------- #

#type_checker = PrettyTable()
#type_checker.set_style(DOUBLE_BORDER)
#type_checker.title = f'{format_str("PASS_BOLD", "STOICHIFY")} - {format_str("WARNING_BOLD", "TYPE CHECKER")}'
#type_checker.field_names = [format_str("BOLD", "SYNTHESIS"), format_str("BOLD", "DECOMPOSITION"), format_str("BOLD", "SINGLE REPLACEMENT"), format_str("BOLD", "DOUBLE REPLACEMENT"), format_str("BOLD", "COMBUSTION")]
#type_checker.add_row([format_str("PASS", "A + B -> AB"), format_str("PASS", "AB -> A + B"), format_str("PASS", "A + BC -> AC + B"), format_str("PASS", "AB + CD -> AD + CB"), format_str("PASS", "A + O2 -> A2O3")])

#print(type_checker)

chemical_equation = input('Enter balanced equation: ').replace(' ', '') # [2]H(2) + O(2) -> [2]H(2)O

split_chemical_equation = chemical_equation.split('->')
reactants = split_chemical_equation[0].split('+')
products = split_chemical_equation[1].split('+')

def get_reactant_numbers(string):
	reactants_coefficients = []
	reactants_subscripts = []

	for i in range(len(reactants)):
		if '[' == string[i]:
			while string[i + 1] != ']':
				reactants_coefficients.append(string[i + 1])
				i += 1
		elif '(' == string[i]:
			while string[i + 1] != ')':
				reactants_subscripts.append(string[i + 1])
				i += 1		

	#for reactant in reactants:
	#	reactant_coefficients = []
	#	reactant_subscripts = []
	#	for i in range(len(reactant)):
	#		if '[' in reactant[i]:
	#			while reactant[i + 1] != ']':
	#				reactant_coefficients.append(reactant[i + 1])
	#				i += 1
	#		elif '(' in reactant[i]:
	#			while reactant[i + 1] != ')':
	#				reactant_subscripts.append(reactant[i + 1])
	#				i += 1
	#	reactants_coefficients.append(''.join(reactant_coefficients))
	#	reactants_subscripts.append(''.join(reactant_subscripts))
	return int(reactants_coefficients)

def get_product_numbers(products):
	products_coefficients = []
	products_subscripts = []

	for product in products:
		product_coefficients = []
		product_subscripts = []
		for i in range(len(product)):
			if '[' in product[i]:
				while product[i + 1] != ']':
					product_coefficients.append(product[i + 1])
					i += 1
			elif '(' in product[i]:
				while product[i + 1] != ')':
					product_subscripts.append(product[i + 1])
					i += 1
		products_coefficients.append(''.join(product_coefficients))
		products_subscripts.append(''.join(product_subscripts))  
	return products_coefficients

chemical_equation_given = input('Enter given: ').split(' ') # 12.3 mol [2]H(2)
chemical_equation_wanted = input('Enter wanted: ') # [2]H(2)O

def calculate_product(given, wanted): # [2]H(2) + O(2) -> [2]H(2)O(2)
	print(given[2])
	print(get_reactant_numbers(given[2]))
	#for reactant in reactants:
	#	if given[2] == reactant:
	#		given_type = get_reactant_numbers(reactants)
	#	if wanted == reactant:
	#		wanted_type = get_reactant_numbers(reactants)
	#for product in products:
	#	if given[2] == product:
	#		given_type = get_product_numbers(products)
	#	if wanted == product:
	#		wanted_type = get_product_numbers(products)
	#print(given_type, wanted_type)
	#calculation = given[0] * (wanted_type / given_type)
	#print(calculation)
	#print(calculation)

calculate_product(chemical_equation_given, chemical_equation_wanted)

