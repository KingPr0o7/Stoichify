#
# Nathan Parker | 5/12/24 | v0.8.0
# Dealing with numbers is hard … especially scientific notation 
# and significant figures. In which this file (precision.py) handles 
# them. With the main purpose of converting numbers already in scientific 
# notation to floats, and vice versa, and to deal with significant figures 
# of those numbers plus floats and integers. Even including rounding to 
# numbers (ints, floats, and scientific numbers) to a specified significant 
# figure amount with log10, as reporting values with the correct user 
# measurement is critical.
#
# Main Libraries:
# - math (Rounding numbers)
# - re (Regular Expressions for pattern matching)
#

import math
import re

class Scientific_Handler():
	"""
	Takes numbers, regardless of their format, and converts them to scientific
	notation or floats (if needed). This is done through some regular expressions and string
	manipulation.
	"""
    
	def __init__(self, number):
		"""
		:param number: The number to convert to scientific notation or a float.
		"""
		
		self.number = number
  
	def to_float(self):
		"""
		Takes any number, and checks to see if it's in scientific notation. 
		If it is, it converts it to a scientific notation float. If not,
		converts to it's corresponding type.
		"""

		number_str = str(self.number)
		match = re.match(r'([0-9.]+)\s*[xXeE*]\s*10\^?([+-]?[0-9]+)', number_str, re.I) # Expanded (e.g. 4.2 x 10^2) 

		if not match:
			match = re.match(r'([0-9.]+)[eE]([+-]?[0-9]+)', number_str, re.I) # Shorthand (e.g. 4.2e2)
		if match:
			base, exponent = match.groups()
			return float(f"{base}e{exponent}")
		else:
			if "." in str(self.number):
				return float(self.number)	
			else:
				return int(self.number)	

	def to_scientific(self):
		"""
		Takes the number, and checks if it can be converted to 
		scientific notation. If it can, it converts it to a 
		presentable scientific notation string.
		"""

		# Split the number on 'e'
		if "e" not in str(self.number).lower():
			if "." in str(self.number): # If it's just a float
				return float(self.number)
			else:
				if len(str(int(float(self.number)))) > 6: 
					self.number = re.sub("e\+0", "e+", f"{float(self.number):.3e}")
				else:
					return "{:,}".format(int(self.number)) # If not, use commas to separate the numbers

		base, exponent = str(self.number).lower().split('e') # If it is in a shorthand scientific notation

		# Convert the exponent to superscript
		superscript_digits = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻") # Translate the digits to superscript
		exponent = exponent.translate(superscript_digits).replace("+", "").replace("^", "") # Replace them, and exclude other symbols

		return f"{base} × 10{exponent}"

class Significant_Figures:
	def __init__(self):
		"""
		Handles all the significant figures calculations, to ensure reports of numbers
		are in the correct precision (not to overstate the accuracy of the data).
		"""
		pass
	
	def parser(self, figure):    
		significant_figures = 0 # Keep track of the significant figures of each number
		figure = Scientific_Handler(figure).to_float() # Convert the number to a float

		if "e" in str(figure).lower(): # If the number is in scientific notation
			figure = str(figure).lower().split("e")[0] 

		if isinstance(figure, str): # If you somehow have your number (including trailing zeros) as a string
			if "." in figure:
				figure = figure.replace(".", "")
				zeros_removed = figure.lstrip("0") # Strip leading zeros
			else:
				zeros_removed = figure.lstrip("0").rstrip("0") # Strip both leading and trailing zeros
			significant_figures = len(zeros_removed)
			return significant_figures
		else: # Regular calculation (assuming trailing zeros are truncated)
			figure_str = str(figure)
			if "." in figure_str:
				# If there's a decimal point, count all digits as significant
				significant_figures = len(figure_str.replace(".", ""))
			else:
				significant_figures = len(figure_str.lstrip("0").rstrip("0")) # Strip leading zeros
		return significant_figures

	def round(self, target_number, sig_figs):
		"""
		Round a number to a certain number of significant figures, 
		answer graciously provided by Evgeny on StackOverflow:
	
		https://stackoverflow.com/a/3411435/20617039 (log10)
	
		:param target_number: The number to round to a certain number of significant figures.
		:param sig_figs: The number of significant figures to round the number to.
		:return: The number rounded to the specified number significant figures.
		"""

		saved_target_number = str(target_number)
	
		if "e" in str(target_number): # If the number is in scientific notation, convert it to a float
			target_number = float(str(target_number).split("e")[0])

		if target_number != 0:
			result = round(target_number, -int(math.floor(math.log10(abs(target_number))) + (1 - sig_figs)))
			if sig_figs <= math.floor(math.log10(abs(target_number))) + 1:
				return int(result)
			else:
				if "e" in saved_target_number:
					result = f"{result}e{saved_target_number.split('e')[1]}" # Ensure scientific notation is preserved as a float
					if "+" in result:
						result = result.replace("+", "")
				return result
		else:
			return 0  # Can't take the log of 0

#
# Some testing done through creation
#

print(type(Scientific_Handler(35).to_float()))
# print(Significant_Figures().parser(1.0))
# print(Significant_Figures().parser(25))
# print(Scientific_Handler(150000000).to_scientific())
# print(Significant_Figures().parser("9.3021 x 10^27"))
# print(Significant_Figures().parser(3.4))
# print(Scientific_Handler(1.23e-4).to_float()) # 0.000123
# print(Scientific_Handler(1.23e4).to_float()) # 12300.0
# print(Scientific_Handler(1.23e4).to_scientific()) # 1.23 × 10⁴
# print(Scientific_Handler("9.3021 x 10^27").to_float()) 
# print(Scientific_Handler("9.3021e27").to_float())
# print(Scientific_Handler("9.3021E27").to_float())
# print(Scientific_Handler("9.3021*10^27").to_float())
# print(Scientific_Handler("9.3021 * 10^-27").to_float())
# print(Scientific_Handler("9.3021e27").to_scientific()) # 1.23 × 10⁻⁴
# print(Significant_Figures().parser(float(9.3021e-27)))