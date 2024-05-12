#
# Nathan Parker | 5/11/24 | v0.8.0
# Regarding this module, its purpose is to instate instances of either equations or substances. 
# With an equation, there is a lot more to consider. Like for instance, substance concatenation, 
# yield arrows, charges, states, matrix building, etc.  But a substance instance is a lot simpler, 
# just with a bit more accessor methods for a more defined mutators later on. Both equations and 
# substances can have stoichiometric calculations performed, but both are extremely diverse.   
#
# Main Libraries:
# - unicodedata: Used to check for UNICODE characters in the equation, like arrows.
# - re: Regular Expressions (String Checking).
# - sympy: Symbolic Mathematics (Equations - https://www.sympy.org/en/index.html).
# - chemlib: Chemical Library (Molar Masses - https://github.com/harirakul/chemlib/tree/master).
#

# Mathematical Libraries
import sympy
from sympy import Matrix, lcm
from chemlib import Element 

# String Handling Libraries
import unicodedata
import re

# Logical Libraries
from precision import Significant_Figures 
from stoichiometry import Stoichify

#
# Constants
#   Required scientific numbers used to bridge needed calculations.
#

STP = 22.4 # Standard Temperature and Pressure (L/mol)
AVOGADRO = 6.02e23 # Avogadro's number (particles/mol)]

# RegEx Patterns
UPPERCASE = "^[A-Z]$"
LOWERCASE = "^[a-z]$"

class Substance():
	"""
	Create an instance of a substance, which is a chemical compound or element.
	In which, you can perform informational extractions, manipulations, and calculations. 
	All pertaining to the substance's properties and characteristics, like its coefficients, 
	subscripts, and elemental makeup which leads to performing stoichiometry measurements conversions.
	"""
	
	def __init__(self, substance):
		"""	
		:param substance: The substance to be analyzed, manipulated, and calculated.
		"""
		self.substance = str(substance) # Stringifed substance, to ensure it's a string
		self.balanced_dict = {substance: self.substance_coefficient()} # Balanced dictionary of the substance
		self.work_shown = [] # Work shown in the stoichiometry calculations
  
	def __str__(self):	# String representation of the substance, used for formatting
		return self.substance
  
	def substance_coefficient(self):
		"""
		Extracts the coefficient of the substance. All
		substances have a coefficient, but if not provided, it's 1 by default, 
		just like with variables in algebra (always placed at the 0th index).
  
		:return: The coefficient of the substance.
		"""
  
		coefficient_match = re.match(r"(\d+)[A-Z]", self.substance) # Match the coefficient of the substance (e.g. 2H2O, 33CO2, etc.)
		coefficient = 1
		if coefficient_match:
			coefficient = int(coefficient_match.group(1))
   
		return coefficient
  
	def remove_coefficients(self):
		"""
		Removes the coefficients from the substance. Where we 
		assume the coefficient is 1, to start calculating the
		elemental balances.
  
		:return: The substance without the coefficient.
 		"""
   
		self.substance = re.sub(r'^\d+(?=[A-Z])', '', self.substance) # Similar to the coefficient method, but we remove it
		return self.substance
  
	def add_subscripts(self):
		"""
		Replace all positive integers in the substance with their
		respective subscript versions. This is only used for display purposes.
  
		:return: The substance with subscripts, instead of integers.
		"""
		subscript_digits = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉") # Translate integers to subscripts
		self.substance = str(self.substance).translate(subscript_digits) # Apply it
		return self.substance

	def replace_subscripts(self):
		"""
		Change back all subscripts to their respective integer versions.
		Usually done to perform calculations with the substance, as 
		subscripts are not recognized as integers.
  
		:return: The substance with integers, instead of subscripts.
		"""
		
		subscript_digits = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789") # Translate it back
		self.substance = str(self.substance).translate(subscript_digits) # Apply it
		return self.substance

	def calculation_presentation(self):
		"""
		Converts the substance to a more presentable form, with subscripts
		and without coefficients, to ensure the substance is properly displayed
		(mostly in dropdowns and work shown in stoichiometry calculations).
  
		:return: The substance in a presentable form.
		"""
		substance = Substance(self.substance) # Initialize a new instance of the substance
		substance.remove_coefficients()
		substance.add_subscripts()
		return str(substance)

	def element_scanner(self, output=None):
		"""
		Takes a string (AKA a substance) and first scans for a capital character.
		Upon finding a capital letter, it checks the next character's capitalization state 
		to see if it's a two-lettered element. If the second character isn't a lowercase 
		character it's a single element. 
	
		:param output: The output of the element scanner, which can be raw
		(includes not found elements marked in "-") or unique (all unique elements).
		:return: A list of elements found in the substance, based on the output param.
		"""
		elements = [] # Only includes found elements
		for index, char in enumerate(self.substance):
			if re.match(UPPERCASE, char):
				element = char
				# Check to see if the character next to the element is lowercase (two-lettered element)
				if index + 1 < len(self.substance) and re.match(LOWERCASE, self.substance[index + 1]):
					element = f"{char}{self.substance[index + 1]}"

				# Check to see if the element is valid (from the periodic table, however isn't foolproof)
				try:
					element_verification = Element(element) 
				except Exception:
					raise Exception(f"Element Verification: The element '{element}' is not found in the periodic table. Please ensure the element is spelled/capitalized correctly.")
	
				if output == "unique":
					# Don't include duplicates
					if element not in elements:
						elements.append(element)
				else:
					elements.append(element)
     
			elif re.match(LOWERCASE, char): # If the character is lowercase, we can't process without context
				continue
			elif str(char).isdigit(): # If it's not a letter, then it's not an element
				if output == "raw":
					elements.append("-")
				else:
					continue

		if len(elements) == 0:
			raise Exception("Element(s) Not Found: No elements were found in the substance. Please ensure the substance is spelled correctly.")

		if all(element == "-" for element in element):
			raise Exception("Element(s) Not Found: No elements were found in the substance. Please ensure the substance is spelled correctly.")

		return elements

	def substance_scanner(self, makeups=None, side=None):
		"""
		Scans through the given substance, first extracting all occurring elements.
		Then, it scans through the substance to find the coefficients, subscripts, and multipliers
		associated with each element.

		:param makeups: An optional dictionary to store the elemental makeup of the substance, on 
		their respective side (reactants or products). If not provided, the function will return the 
  		elemental makeup of the substance. With each entry looking like: 'Al': [('Al', (1, 1, 1))].
		Where the tuple is the coefficient, subscript, and multiplier of the element in the substance.
  
		:param side: The side of the chemical equation the substance is on (reactants or products).
		Provide this parameter if you're using the makeups parameter.

		:return: Gives the elemental makeup of the substance, stored in the makeups dictionary, if provided.
		"""

		substance_coefficient = 1
		element_multiplier = 1 # If parentheses aren't detected, the subscript is 1 by default
		elements = self.element_scanner("raw") # Get all occurring not found and found elements
		element_index = 0
  
		if makeups != None:
			makeups[side][self.substance] = []
		substance_elemental_makeup = []
 
		for index, char in enumerate(self.substance):
			element_subscript = 1 # Same as coefficients; if not provided; it's 1.
			string_dilation = 1 # Used to traverse the string

			if re.match(LOWERCASE, char):
				continue
			elif char == "(":
				closing_parenthesis_index = str(self.substance).index(")")
				element_multiplier = int(self.substance[closing_parenthesis_index + 1])
				continue
			elif char == ")":
				element_multiplier = 1 # Reset the multiplier
				continue
			elif char == "[" or char == "]": # If a closing bracket is detected, it's a complex ion
				continue
			elif char != "(" and char != ")":
				if element_index < len(elements):
					element = elements[element_index] # Get the element from the elements list
					element_index += 1
	
					if element == "-": # Ignore elements that aren't found (trust me bro, the scanner works (at least I hope))
						continue
					else:
						if len(element) == 2: # Move pointer over 2, to get to the end of the two-lettered elements
							string_dilation = 2
							if string_dilation + index > len(self.substance) - 1: # Ensure range
								string_dilation = 1
						if index + 1 < len(self.substance) and str(self.substance[index + string_dilation]).isdigit(): # Check if next char is a number, while in range.
							# Account for multiple digit subscripts (e.g. C6H12O6, C12H22O11, etc.)
							subscripts = ""
							subscript_index = index + string_dilation
							while subscript_index < len(self.substance) and str(self.substance[subscript_index]).isdigit(): # Loop through as long as the next character is a number
								subscripts += self.substance[subscript_index]
								subscript_index += 1
							element_subscript = int(subscripts)
						else: # If not a number, the subscript is 1.
							element_subscript = element_subscript
						element_data = (substance_coefficient, element_subscript, element_multiplier)
						if makeups != None:
							if side == "reactants" or side == "products":
								makeups[side][self.substance].append((element, element_data))
						else:
							substance_elemental_makeup.append((element, element_data))
						
		if makeups == None:
			return substance_elemental_makeup
		else:
			return makeups

	def measurement_converter(self, amount, measurement, type, work_shown: list):
		"""
		Take a substance's measurement (L, r.p., g), and amount and
		turn it into moles (mol). All with predefined scientific constants,
		like STP, Avogadro's number, and the molar masses of elements. All molar masses
		are provided by the chemlib library to ensure accuracy and precision in the calculations
		(https://github.com/harirakul/chemlib/tree/master).
  
		:param amount: The amount of the substance, you have (usually a float or integer).
		:param measurement: The measurement of the substance (L, r.p., g).
		:param type: The type of conversion (* (multiplication), / (division)).
		:return: The amount of the substance in moles, and the significant figures after conversion.
		"""

		# Imported here to avoid circular imports
		from precision import Scientific_Handler # Import the scientific handler to for changing numbers into scientific notation (if needed)
		current_substance = Substance(self.substance).calculation_presentation() # Put it in a presentable form

		#
		# Calculation + Presentation
		#   Below the code takes a measurement and amount, and based on type calculates it.
		#   Moreover, the type also applies to the presentation of the fraction, which is 
		#   required for each type. 
 
		if measurement == "L": # Liters to moles
			amount = amount * STP if type == "*" else amount / STP if type == "/" else amount
			if type == "*":
				work_shown = f"{STP}L {current_substance}", f"1 mol {current_substance}"
			elif type == "/":
				work_shown = f"1 mol {current_substance}", f"{STP}L {current_substance}"
		elif measurement == "r.p.": # Atoms / Representative Particles to moles
			amount = amount * AVOGADRO if type == "*" else amount / AVOGADRO if type == "/" else amount 
			if type == "*":
				work_shown.append((f"{Scientific_Handler(float(AVOGADRO)).to_scientific()} r.p. {current_substance}", f"1 mol {current_substance}"))
			elif type == "/":
				work_shown.append((f"1 mol {current_substance}", f"{Scientific_Handler(float(AVOGADRO)).to_scientific()} r.p. {current_substance}"))
		elif measurement == "g": # Grams to moles
			elemental_makeup = self.substance_scanner()
			molar_masses = []
			molar_mass = 0

			# Get the molar mass of each element in the substance (also accounts for the subscript)
			for element in elemental_makeup:
				atomic_mass = Element(element[0]).properties['AtomicMass'] # Get the atomic mass of the element to be converted to molar mass
				molar_masses.append(atomic_mass)
				molar_mass += atomic_mass * element[1][1] * element[1][2] # Calculate the molar mass of the substance (subscript * multiplier * atomic mass)

			amount = amount * molar_mass if type == "*" else amount / molar_mass if type == "/" else amount
			if type == "*":
				work_shown.append((f"{molar_mass} g {current_substance}", f"1 mol {current_substance}"))
			elif type == "/":
				work_shown.append((f"1 mol {current_substance}", f"{molar_mass}g {current_substance}"))

		return amount

	def stoichify(self, given_amount, given_significant_figures, given_measurement, given_substance, wanted_measurement, wanted_substance):
		"""
		Performs the stoichiometry calculations, with all given and wanted parameters, 
		to convert the given substance to the wanted substance. While also reporting all
		number in the correct significant figures, to ensure the maximum precision and accuracy.
  
		:param given_amount: The amount of the given substance. You can input a float or integer;
		however, if you have a scientific number (e.g. 4.2 x 10^2), you must input it as a string,
		like "4.2 x 10^2" OR "4.2e2" so it can be converted to a float.

		:param given_significant_figures: The significant figures of the given amount.
		:param given_measurement: The measurement of the given substance (L, r.p., g).
		:param given_substance: The given substance to convert to the wanted substance.
		:param wanted_measurement: The measurement of the wanted substance (L, r.p., g).
		:param wanted_substance: The wanted substance to convert the given substance to.
		:return: The amount of the wanted substance, with the amount (in the correct significant figures) and the measurement with substance (e.g. 42.8 g H2O).
		"""

		answer, self.work_shown = Stoichify(self.balanced_dict, self.work_shown).solve(given_amount, given_significant_figures, given_measurement, given_substance, wanted_measurement, wanted_substance)
		return answer, self.work_shown

class Equation():
	"""
	Make an instance of a chemical equation, where each part of the equation is tracked,
	and processed to be balanced. Ensuring that calculations are accurate and considerate 
	of the molar ratios, and convert amounts of reactants and or products! Each stage, 
	(original, unbalanced, and balanced), elements (unique), reactants, products 
	(and their elemental makeups), substances, the element matrix, and balanced 
	coefficients are tracked and can be easily retrieved. 
	
	Upon defining the equation, the program will AUTOMATICALLY balance the equation, and provide it!
	"""
	
	def __init__(self, equation):
		"""
		:param equation: The chemical equation to be balanced.
		"""

		self.original = equation # User's inputted chemical equation
		self.unbalanced = equation # Equation put through the type checking process
		self.elements = [] # All elements (uniques) within the chemical equation
		self.reactants = []
		self.products = []
		self.makeups = { # Elemental makeups (coefficients, subscripts, multipliers) of the reactants and products
			"reactants": {},
			"products": {}, 
		}
		self.substances = [] # All substances within the chemical equation 
		self.element_matrix = [] # Amounts of each substance on both sides of the equation
		self.balanced_coefficients = [] # Balanced coefficients for each substance
		self.balanced = "" # Final balanced chemical equation in presentable form
		self.balanced_dict = {} # Balanced dictionary for each substance
		self.work_shown = [] # Work shown in the stoichiometry calculations (fractions and single line strings)
		self.balance() # Automatically balance the equation upon initialization

	def replace_arrows(self): #→⮕⇨🡒🡒⟶➜➔➝➞➨⭢🠂🠂🠊🠢🠦🠦🠮🠮🠒🠖🠚🠞🡢🡪🡲🡺
		"""
		Standardizes the arrow representation in the equation, removing any UNICODE arrow 
		and replacing it with '→'. The standard arrow for 'yields' in Chemistry.
  
		:return: The equation with the standardized arrow representation.
		"""
		self.unbalanced = ''.join(['→' if 'arrow' in unicodedata.name(char).lower() else char for char in self.unbalanced]) # Match all unicodes with 'arrow' in their name
		self.unbalanced = self.unbalanced.replace('->', '→') # Replace with the standard chemistry yield arrow

		# They didn't use the standard arrow, so raise an exception
		if '→' not in self.unbalanced:
			raise Exception("'Yields' Arrow Check: The yields or any UNICODE arrow is not found in the equation. Please use '->' or '→' to represent the yields arrow, so the program can properly parse reactants and products.")
		
		return self.unbalanced

	def detect_charges(self):
		"""
		Finds if the user included substance charges in the equation, and rejects
		the equation if it does. Stoichify does not support charges in the equation, as 
		oxidation-reduction reactions require a different approach to balance.
  
		:return: The equation without any charges, if found.
		"""

		negative_charges = ['-', '−']

		plus_count = self.unbalanced.count('+')
		delta = (len(self.substances) - 1) - plus_count # Find if each substance has a plus after it
		if delta > 2: # If the delta doesn't equal 2, then there are charges in the equation
			raise Exception("Equation Charges Check: Your equation includes charges (Oxidation-Reduction Reactions), which are not supported by Stoichify.")

		# Also check negatives
		for substance in self.substances:
			if any(char in substance for char in negative_charges):
				raise Exception("Equation Charges Check: Your equation includes charges (Oxidation-Reduction Reactions), which are not supported by Stoichify.")

	def check_concatenation(self):
		"""
		Checks if the user properly concatenated substances in the equation using the '+' symbol.
		If not, the program will reject the equation and prompt the user to use '+' to separate substances,
		so the program can properly parse reactants and products.
  
		:return: Only raises exceptions if the equation is not properly concatenated or has an empty substance.
		"""

		# If forgotten, the program will reject the equation
		if '+' not in self.unbalanced:
			raise Exception("Substance Concatenation '+' Check: The '+' symbol is not found in the equation. Please use '+' to separate substances in the equation.")

		# If there's an empty substance, also report an exception
		for substance in self.substances:
			if len(substance) == 0:
				raise Exception("Substance Concatenation Length Check: There is an empty substance in the equation. Please remove the empty substance, and carefully type the equation again.")

	def remove_states(self):
		"""
		Removes all substance states in the equation, such as (s), (l), (g), and (aq).
		As the Stoichify does not need to know the state of the substance to balance the equation.
  
		:return: The equation without any substance states.
		"""

		substance_states = ['\([slgaq]*\)', '\([SLGAQ]*\)'] # RegEx for substance states
		for state in substance_states:
			self.unbalanced = re.sub(state, "", self.unbalanced) # Replace em'
		return self.unbalanced

	def type_checker(self):
		"""
		A series of checks to ensure the user inputted a valid chemical equation,
		that can be parsed and balanced by Stoichify. If the equation passes all checks, the program
		will proceed.

		:return: The equation after passing all checks (arrow, charges, concatenation, and states).
		"""

		# Ensure format for scanners and matrix building
		self.replace_arrows()
		self.detect_charges()
		self.remove_states()
  
		# Split the equation into its reactants and products
		self.reactants = self.unbalanced.replace(" ", "").split("→")[0].split("+")
		self.products = self.unbalanced.replace(" ", "").split("→")[1].split("+")

		self.substances = []
  
		for substance in self.reactants + self.products:
			new_substance = Substance(substance)
			self.substances.append(new_substance.remove_coefficients()) # We don't need coefficients to balance the equation

		self.check_concatenation()
  
		self.substances_arrowed = self.reactants + ["→"] + self.products
		return self.unbalanced

	def substance_element_makeups(self, side):
		"""
		Scans through the substances of the side (reactants or products) and extracts the
		elemental makeup of each substance. Also collects all unique elements in the equation.
  
		:param side: The side of the chemical equation the substance is on (reactants or products).
		:return: The elemental makeup of the substance, stored in the makeups dictionary of the side.
		"""

		elements_side = ""
		if side == "reactants":
			elements_side = self.reactants
		else:
			elements_side = self.products
 
		for substance in elements_side:
			substance = Substance(substance)
			substance.remove_coefficients() # Remove the coefficients from the substance, as we assume they're 1 (because the equation is unbalanced)
			self.makeups = substance.substance_scanner(self.makeups, side) # Calculate the elemental makeup of the substance on that side
   
			# Get all unique elements in the equation, while we're at it
			elements = substance.element_scanner("unique")
			for element in elements:
				if element not in self.elements:
					self.elements.append(element)

		return self.makeups[side]

	def matrix_builder(self, side):
		"""
		Creates a matrix (2D Array) of each element's amount (subscript * multiplier) 
		in each substance of the side (reactants or products (-1 to distinguish between the two)).
  
		:param side: The side of the chemical equation the substance is on (reactants or products).
		:return: The element matrix of the side.
		"""

		for substance in self.makeups[side]: # For each substance in the side
			matrix_row = []
			for element in self.elements: # Get all unique elements in the equation
				element_total = 0
				for substance_element in self.makeups[side][substance]: # See if the element is in the substance on that side
					if substance_element[0] == element: # See if the element is in the substance, uniquely.
						if side == "reactants":
							element_total += substance_element[1][1] * substance_element[1][2]
						else:
							element_total += substance_element[1][1] * substance_element[1][2] * -1 # Exclude negatives + designate products
				matrix_row.append(element_total) # Add totals until a row is formed
			self.element_matrix.append(matrix_row) # Make a new row to define a matrix (2D array)
		return self.element_matrix

	def matrix_solver(self):
		"""
		Solves the matrix of the element amounts in each substance of the reactants and products.
		Then, the program uses linear algebra to solve the matrix and get the balanced coefficients.
		This wouldn't be possible without the use of matrices and linear algebra by Mohammad-Ali Bandzar:
   
		https://medium.com/swlh/balancing-chemical-equations-with-python-837518c9075b
  
		:return: The balanced coefficients of each substance in the equation (a list of integers, in order).
		"""
	 
		# Use smypy to solve the matrix via linear algebra (Thanks to Mohammad-Ali Bandzar for this logic/code)
		matrix = Matrix(self.element_matrix)
		matrix = matrix.transpose() # Swap the rows and columns
		try:
			solution = matrix.nullspace()[0] # Solve the matrix
		except Exception:
			raise Exception("Matrix Solver: The matrix is singular, and cannot be solved. Please ensure the equation is properly typed.")
		multiple = lcm([val.q for val in solution]) # Find the least common multiple (LCM) of the denominators 
		balanced_coefficients = multiple * solution # Multiply by LCM to remove fractions (either solution is valid)     
		
		return balanced_coefficients

	def reconstruct(self, balanced_coefficients, include_one=True):
		"""
		Reconstructs the balanced chemical equation into a more human-readable format.
		Done by reconstructing the substances with their balanced coefficients, and substituting
		the integer subscripts with their respective subscript versions.
  
		:param balanced_coefficients: The balanced coefficients of each substance in the equation, 
		provided by the matrix_solver.
		:param include_one: A boolean to include the coefficient if it's 1, or exclude it. Most chemists
		exclude the coefficient of one, similar to mathematicians in algebra.
  
		:return: The balanced chemical equation, with the coefficients and subscripts.
		"""
		pointer = 0
	
		for index, substance in enumerate(self.substances_arrowed):
			if substance != "→":
				# Reconstruct via Substance instances
				substance = Substance(substance)
				substance.remove_coefficients()
				substance.add_subscripts()
	
				# Element basis (if they want 1s included, or not)
				element_builder = f"{balanced_coefficients[pointer]}{substance}"
				if include_one == False and balanced_coefficients[pointer] == 1:
					element_builder = f"{substance}"
	
				if index == len(self.substances_arrowed) - 1:
					self.balanced += f"{element_builder}"
				else:
					# Ensure correct formatting (e.g. no '+' at the end of the equation)
					if self.substances_arrowed[index + 1] != "→":
						self.balanced += f"{element_builder} + "
					else:
						self.balanced += f"{element_builder} "
				pointer += 1
			else:
				self.balanced += "→ " # Add the 'yields' arrow back in
		return self.balanced

	def balance(self, include_one=True):
		"""
		Performs checks, scans, and calculations from previous methods, to balance 
		the chemical equation. Whilst all properties of the equation are tracked 
		and stored for easy access.
  
		:param include_one: A boolean to include the coefficient if it's 1, or exclude it. Most chemists
		exclude the coefficient of one, similar to mathematicians in algebra.

		:return: The balanced chemical equation, with the coefficients and subscripts.
		"""

		# Ensure the equation is properly formatted
		self.type_checker()
  
		# Get the elemental makeup of each substance on both sides of the equation
		self.substance_element_makeups("reactants")
		self.substance_element_makeups("products")
  
		# Build the matrix of the element amounts in each substance of the reactants and products
		self.matrix_builder("reactants")
		self.matrix_builder("products")
  
		# Solve the matrix to get the balanced coefficients
		self.balanced_coefficients = self.matrix_solver()
		self.balanced = self.reconstruct(self.balanced_coefficients, include_one)
		
		self.balanced_dict = dict(zip(self.substances, self.balanced_coefficients)) # Balanced dictionary for each substance (used for stoichiometry calculations)
		return self.balanced

	def stoichify(self, given_amount, given_significant_figures, given_measurement, given_substance, wanted_measurement, wanted_substance):
		"""
		Performs the stoichiometry calculations, with all given and wanted parameters, 
		to convert the given substance to the wanted substance. While also reporting all
		number in the correct significant figures, to ensure the maximum precision and accuracy.
  
		:param given_amount: The amount of the given substance. You can input a float or integer;
		however, if you have a scientific number (e.g. 4.2 x 10^2), you must input it as a string,
		like "4.2 x 10^2" OR "4.2e2" so it can be converted to a float.
		:param given_significant_figures: The significant figures of the given amount.
		:param given_measurement: The measurement of the given substance (L, r.p., g).
		:param given_substance: The given substance to convert to the wanted substance.
		:param wanted_measurement: The measurement of the wanted substance (L, r.p., g).
		:param wanted_substance: The wanted substance to convert the given substance to.
		:return: The amount of the wanted substance, with the amount (in the correct significant figures) and the measurement with substance (e.g. 42.8 g H2O).
		"""
  
		answer, self.work_shown = Stoichify(self.balanced_dict, self.work_shown).solve(given_amount, given_significant_figures, given_measurement, given_substance, wanted_measurement, wanted_substance)
		return answer, self.work_shown


#
# Testing done through the creation of this module
#

#if __name__ == "__main__":
	# equation = Equation("Al + Cl2 → AlCl3")
	# print(equation.stoichify(42.8, 3, "g", "2Al", "g", "3Cl2"))
	
	# equation = Equation("K + H2O → KOH + H2")
	# print(equation.stoichify(7.99, 3, "mol", "KOH", "r.p.", "H2O"))
	# print(equation.balanced)
	# print(equation.balanced_dict)
	
	# equation = Equation("C3H8 + O2 → CO2 + H2O")
	# print(equation.stoichify(2.8, 2, "mol", "C3H8", "g", "CO2"))
	
	# print(Significant_Figures().parser("9.3021 x 10^27")[1])
	# print(Significant_Figures().parser("9.3021e27")[1])
	# print(Significant_Figures().parser("9.3021 * 10^+27")[1])
	# print(Significant_Figures().parser("9.3021 * 10^-27")[1])
	# from stoichiometry import scientific_handler
	# print(scientific_handler("2.716 x 10^24"))
	# print(scientific_handler(float(AVOGADRO)))
 
	# substance = Substance("F2")
	# print(substance.stoichify("9.3021 x 10^27", 5, "r.p.", "F2", "g", "F2"))

	# substance = Substance("H2O")
	# print(substance.measurement_converter(1, "r.p.", "/", []))

	# substance = Substance("NH4Cl")
	# print(substance.stoichify("3.902 x 10^28", 4, "r.p.", "NH4Cl", "g", "NH4Cl"))
 
	# equation = Substance("F2")
	# print(equation.stoichify("9.3021 x 10^27", 5, "r.p.", "F2", "g", "F2"))
 
	# substance = Substance("S")
	# print(substance.stoichify(4.2, 2, "mol", "S", "g", "S"))
	
	# print(Significant_Figures().round(15446.502406121414, 5))
 
	# substance = Substance("OCl2")
	# print(substance.stoichify(392.1, 4, "g", "OCl2", "r.p.", "OCl2"))
	
	# substance = Substance("F2")
	# print(substance.stoichify("9.3021 x 10^27", 5, "r.p.", "F2", "g", "F2"))
	
	# substance = Substance("H2O")
	# print(substance.element_scanner())
	
	# equation = Equation("H2O + 2 -> H2O")
	# print(equation.balanced)
 
	# substance = Substance("K4[Fe(SCN)6]")
	# print(substance.element_scanner("raw"))
	# equation = Equation("K4[Fe(SCN)6] + K2Cr2O7 + H2SO4 → Fe2(SO4)3 + Cr2(SO4)3 + CO2 + H2O + K2SO4 + KNO3")
	# print(equation.balanced)
	# equation = Equation("H2 + O2 → H2O")
	# equation.balance()
	# substance = Substance("H2O")
	# print(substance.substance_scanner(equation.makeups, "products"))
	# print(equation.makeups)