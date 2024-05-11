import math # Mathematics (Rounding)
import re # Regular Expressions (Pattern Matching)
import decimal

class Scientific_Handler():
	def __init__(self, number):
		self.number = number
  
	def to_float(self):
		"""
		Converts a scientific number to a float.
		"""
		number_str = str(self.number)
		match = re.match(r'([0-9.]+)\s*[xXeE*]\s*10\^?([+-]?[0-9]+)', number_str, re.I)
		if not match:
			match = re.match(r'([0-9.]+)[eE]([+-]?[0-9]+)', number_str, re.I)
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
		Converts a float to a scientific number.
		"""
		# Split the number on 'e'
		if "e" not in str(self.number):
			if "." in str(self.number):
				return float(self.number)
			else:
				if len(str(int(self.number))) > 6:
					self.number = re.sub("e\+0", "e+", f"{self.number:.3e}")
				else:
					return "{:,}".format(int(self.number))
		base, exponent = str(self.number).split('e')

		# Convert the exponent to superscript
		superscript_digits = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
		exponent = exponent.translate(superscript_digits).replace("+", "").replace("^", "")

		return f"{base} × 10{exponent}"

class Significant_Figures:
	def __init__(self):
		"""
		Handles all the significant figures calculations, to ensure reports of numbers
		are in the correct precision (not to overstate the accuracy of the data).
		"""
		pass
	
	def parser(self, figure):    
		significant_figures = [] # Keep track of the significant figures of each number
		figure = Scientific_Handler(figure).to_float() # Convert the number to a float

		if "e" in str(figure): # If the number is in scientific notation
			figure = str(figure).split("e")[0] # Split the number on 'e'
  
		if isinstance(figure, str): # If you somehow have your number (including trailing zeros) as a string
			if "." in figure:
				figure = figure.replace(".", "")
				zeros_removed = figure.lstrip("0") # Strip leading zeros
			else:
				zeros_removed = figure.lstrip("0").rstrip("0")
			significant_figures = len(zeros_removed)
			return significant_figures
		else: # Regular calculation (assuming trailing zeros are truncated)
			if "." in str(figure):
				figure = str(figure).replace(".", "")
				zeros_removed = figure.lstrip("0").rstrip("0") # Strip leading and trailing zeros
				significant_figures = len(zeros_removed) # Add the significant figures of the number to the known list
			else:
				significant_figures = len(str(figure).lstrip("0").rstrip("0")) # Strip leading zeros
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
	
		if "e" in str(target_number):
			target_number = float(str(target_number).split("e")[0])

		if target_number != 0:
			result = round(target_number, -int(math.floor(math.log10(abs(target_number))) + (1 - sig_figs)))
			if sig_figs <= math.floor(math.log10(abs(target_number))) + 1:
				return int(result)
			else:
				if "e" in saved_target_number:
					result = f"{result}e{saved_target_number.split('e')[1]}"
					if "+" in result:
						result = result.replace("+", "")
				return result
		else:
			return 0  # Can't take the log of 0

print(Significant_Figures().parser(25))
print(Scientific_Handler(150000000).to_scientific())
print(Significant_Figures().parser("9.3021 x 10^27"))
print(Significant_Figures().parser(3.4))
# print(Scientific_Handler(1.23e-4).to_float()) # 0.000123
# print(Scientific_Handler(1.23e4).to_float()) # 12300.0
# print(Scientific_Handler("9.3021 x 10^27").to_float()) 
# print(Scientific_Handler("9.3021e27").to_float())
# print(Scientific_Handler("9.3021E27").to_float())
# print(Scientific_Handler("9.3021*10^27").to_float())
# print(Scientific_Handler("9.3021 * 10^-27").to_float())
# print(Scientific_Handler("9.3021e27").to_scientific()) # 1.23 × 10⁻⁴

print(Significant_Figures().parser(float(9.3021e-27)))