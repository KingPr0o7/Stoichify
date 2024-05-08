import math # Mathematics (Rounding)

class Significant_Figures:
	def __init__(self):
		"""
		Handles all the significant figures calculations, to ensure reports of numbers
		are in the correct precision (not to overstate the accuracy of the data).
		"""
		pass

	def count(self, figures: list, mode):
		"""
		Count the significant figures of a number, or a list of numbers.
		Mode can be either +, -, *, or / to determine the significant figures 
		of the number(s) based on the operation. 
	
		With addition and subtraction, the number with the least decimal places,
		where multiplication and division, the number with the least significant figures.

		Keep in mind, trailing zeros (e.g. "42.0000") are truncated, as they're not considered significant
		(in Python). You need to find a way to keep track of user input through key presses, and build an
		array into a string to keep track of unaccounted for significant figures (as tkinter does).
	
		:param figures: The number or list () of numbers to count the significant figures of.
		:param mode: The mode of the calculation (+, -, *, /).
		:return: The significant figures of the number(s) (int) and the number(s) (float or int
		"""

		significant_figures = [] # Keep track of the significant figures of each number
		if isinstance(figures[0], str): # If you somehow have your number (including trailing zeros) as a string
			if mode == "*" or mode == "/":
				if "." in figures[0]:
					figure = figures[0].replace(".", "")
					zeros_removed = figure.lstrip("0") # Strip leading zeros
				else:
					zeros_removed = figures[0].lstrip("0").rstrip("0")
				significant_figures = len(zeros_removed)
				return significant_figures, figures[0] # Return the significant figures of that number and the number itself
		else: # Regular calculation (assuming trailing zeros are truncated)
			for figure in figures:
				if "." in str(figure):
					if mode == "+" or mode == "-":
						significant_figures.append(len(str(figure).split(".")[1]))
					elif mode == "*" or mode == "/":
						figure = str(figure).replace(".", "")
						zeros_removed = figure.lstrip("0").rstrip("0") # Strip leading and trailing zeros
						significant_figures.append(len(zeros_removed)) # Add the significant figures of the number to the known list
				else:
					if mode == "+" or mode == "-":
						significant_figures.append(0)
		if mode == "+" or mode == "-": 
			significant_figures = min(significant_figures) # Find lowest decimal place
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
					result = f"{result} x 10^{saved_target_number.split('e')[1]}"
					if "+" in result:
						result = result.replace("+", "")
				return result
		else:
			return 0  # Can't take the log of 0