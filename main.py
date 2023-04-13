import os
import re
from prettytable import PrettyTable
from prettytable import SINGLE_BORDER
from prettytable import DOUBLE_BORDER

# Used for clearing the console. (Replit uses Linux) 
system = 'Windows'

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

type_checker = PrettyTable()
type_checker.set_style(DOUBLE_BORDER)
type_checker.title = f'{format_str("PASS_BOLD", "STOICHIFY")} - {format_str("WARNING_BOLD", "TYPE CHECKER")}'
type_checker.field_names = [format_str("BOLD", "COEFFICIENTS"), format_str("BOLD", "SUBSCRIPTS")]
type_checker.add_row([format_str("PASS", "[1]Ni"), format_str("PASS", "[1]NiBr(4)")])
type_checker.add_row([format_str("PASS", "[12]Ni"), format_str("PASS", "[1]H(2)O")])
type_checker.add_row([format_str("FAIL", "Ni"), format_str("FAIL", "[1]NiBr4")])
print(type_checker)

chemical_equation = input('Enter balanced equation: ').replace(' ', '') # [1]NiBr(4) + [4]K -> [1]Ni + [4]KBr
split_chemical_equation = chemical_equation.split('->')
reactants = split_chemical_equation[0].split('+')
products = split_chemical_equation[1].split('+')

def get_coefficients(string):
	reactants_coefficients = ''

	for i in range(len(string)):
		if '[' == string[i]:
			while string[i + 1] != ']':
				reactants_coefficients += string[i + 1]
				i += 1
	return int(reactants_coefficients)

chemical_equation_given = input('Enter given: ').split(' ') # 12.3 mol [2]H(2)
chemical_equation_wanted = input('Enter wanted: ') # [2]H(2)O

def calculate_product(given, wanted): # [2]H(2) + O(2) -> [2]H(2)O(2)
	calculation = float(given[0]) * (get_coefficients(wanted) / get_coefficients(given[2]))
	calculation = f'{calculation} {given[1]} {wanted[3:5]}'
	return calculation

print(f'\nAnswer: {chemical_equation_given[0]} {chemical_equation_given[1]} {chemical_equation_given[2]} = {calculate_product(chemical_equation_given, chemical_equation_wanted)}')
