import math # Mathematics (Rounding)
import re # Regular Expressions (Pattern Matching)

class Significant_Figures:
	def __init__(self):
		"""
		Handles all the significant figures calculations, to ensure reports of numbers
		are in the correct precision (not to overstate the accuracy of the data).
		"""
		pass

	def parser(self, figure):
		"""
		Parse the given number to count the significant figures of the number(s) and
		calculate into a float or integer.

		Keep in mind, trailing zeros (e.g. float(42.0000)) are truncated, as they're not considered significant
		(in Python). You need to find a way to keep track of user input through key presses, and build an
		array representation or a string just to keep track of unaccounted for significant figures (as tkinter does).
	
		:param figures: The number or list () of numbers to count the significant figures of.
		:return: The significant figures of the number(s) (int) and the number(s) (float or int).
		"""

		significant_figures = [] # Keep track of the significant figures of each number
		calculated_figure = 0 # Float or integer of the number
		if not isinstance(figure, str):
			figure = str(figure)

		# Remove all spaces and replace 'x' with '*'
		figure = figure.replace(" ", "").replace("x", "*")

		# Check if the figure is in scientific notation
		match = re.match(r"(\d*\.?\d*)(e|\*10\^)(\d+)", figure)

		if match:
			significant_figures = len(match.group(1).replace(".", "").lstrip("0").rstrip("0"))
			calculated_figure = float(f"{match.group(1)}e{match.group(3)}")
		else:
			# If not in scientific notation, just count the significant figures
			significant_figures = len(figure.replace(".", "").lstrip("0"))
			calculated_figure = float(figure)

		return significant_figures, calculated_figure

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
					result = f"{result} x 10^{saved_target_number.split('e')[1]}"
					if "+" in result:
						result = result.replace("+", "")
				return result
		else:
			return 0  # Can't take the log of 0