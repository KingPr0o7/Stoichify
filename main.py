import os
import re
from prettytable import PrettyTable
from prettytable import DOUBLE_BORDER

pattern = '[0-9\[\]]'

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

type_checker = PrettyTable()
type_checker.set_style(DOUBLE_BORDER)
type_checker.title = f'{format_str("PASS_BOLD", "STOICHIFY")} - {format_str("WARNING_BOLD", "TYPE CHECKER")}'
type_checker.field_names = [format_str("BOLD", "COEFFICIENTS"), format_str("BOLD", "SUBSCRIPTS"), format_str("BOLD", "FORMULAS")]
type_checker.add_row([format_str("PASS", "[1]Ni"), format_str("PASS", "[1]NiBr(4)"), format_str("PASS", "A + Z -> AZ")])
type_checker.add_row([format_str("PASS", "[12]Ni"), format_str("PASS", "[1]H(2)O"), format_str("PASS", "AZ -> A + Z")])
type_checker.add_row([format_str("FAIL", "3Ni"), format_str("FAIL", "[1]NiBr4"), format_str("PASS", "AZ + Y -> AY + Z")])
type_checker.add_row([format_str("FAIL", "H"), format_str("FAIL", "[1]H20"), format_str("PASS", "AZ + YX -> AX + YZ")])
type_checker.add_row([format_str("FAIL", "Ne"), format_str("FAIL", "[1]Cl2"), format_str("PASS", "C(NUM)H(NUM) + O(2) -> CO(2) + H(2)O")])

error_table = PrettyTable()
error_table.set_style(DOUBLE_BORDER) 

def error_detector(eq_type, error_type, string):
	if error_type == 'format':
		error_table.title = f'{format_str("PASS_BOLD", "STOICHIFY")} - {format_str("FAIL_BOLD", "EQUATION FORMAT ERROR(S)")}'
		error_table.field_names = [format_str('PASS_BOLD', 'EXAMPLE OF WANTED'), format_str('FAIL_BOLD', 'GIVEN')]
	elif error_type == 'coefficient':
		error_table.title = f'{format_str("PASS_BOLD", "STOICHIFY")} - {format_str("FAIL_BOLD", "COEFFICIENT ERROR(S)")}'
		error_table.field_names = [format_str('PASS_BOLD', 'EXAMPLE OF WANTED'), format_str('FAIL_BOLD', 'GIVEN'), format_str('BOLD', 'TYPE')]
		if '[' not in string:
			error_table.add_row([format_str('PASS', '[1]H(2)O'), format_str('FAIL', string), format_str('BOLD', f'[{str(eq_type).upper()}]')])

def calculate_product(given, wanted): # [2]H(2) + O(2) -> [2]H(2)O(2)
	calculation = float(given[0]) * (get_coefficients(wanted) / get_coefficients(given[2]))
	wanted = re.sub(r'\[\d+\]', '', wanted)
	calculation = f'{format_str("PASS_BOLD", f"{calculation} {given[1]} {wanted}")}'
	return calculation

# --------------------------------------------------------------- #
print(type_checker)

chemical_equation = input(f'{format_str("BOLD", "Enter Balanced Equation")}: ').replace(' ', '') # [2]NO + [1]O(2) -> [2]NO(2)
split_chemical_equation = chemical_equation.split('->')  
reactants = split_chemical_equation[0].split('+')
products = split_chemical_equation[1].split('+')

for index, reactant in enumerate(reactants):
    error_detector('reactant', 'coefficient', reactant)

for index, product in enumerate(products):
    error_detector('product', 'coefficient', product)

if error_table._rows:
	print(error_table)
	error_table.clear()

def get_coefficients(string):
	reactants_coefficients = ''

	for i in range(len(string)):
		if '[' == string[i]:
			while string[i + 1] != ']':
				reactants_coefficients += string[i + 1]
				i += 1
	return float(reactants_coefficients)

chemical_equation_given = input(f'{format_str("BOLD", "Enter Given")}: ').split(' ') # 12.3 mol [2]H(2)
chemical_equation_wanted = input(f'{format_str("BOLD", "Enter Wanted")}: ') # [2]H(2)O

print(f'\n{format_str("BOLD", "Answer")}: {chemical_equation_given[0]} {chemical_equation_given[1]} {chemical_equation_given[2]} = {calculate_product(chemical_equation_given, chemical_equation_wanted)}')
