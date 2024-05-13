#
# Nathan Parker | 5/12/24 | v0.8.0
# In the vast complexity of stoichiometry, this module helps solve the 
# equations for you. Once you have created the balanced chemical equation, 
# or have your substance, you initialize the Stoichify class with your values 
# and get your answer. It only has one method and one purpose, to solve 
# stoichiometry problems. 
#
# Main Libraries:
# - None

class Stoichify:
	"""
	Handles all the stoichiometry calculations, converting the given measurement 
	(if not in moles) to moles, then using the molar bridge to convert the
	moles to the wanted measurement. All while considering each the significant 
	figures (weather that be in addition, subtraction, division or multiplication),
	throughout the calculations, to ensure the provided maximum precision and accuracy.
	"""

	def __init__(self, balanced_dict, work_shown: list):
		"""
		Initializes the Stoichify object, with the balanced_dict and work_shown list.

		:param balanced_dict: The balanced dictionary, with the substances as keys and their coefficients as values.
		:param work_shown: The list of work shown, to keep track of the calculations and steps taken.
		"""
		self.balanced_dict = balanced_dict
		self.work_shown = list(work_shown)

	def solve(self, given_amount, given_significant_figures, given_measurement, given_substance, wanted_measurement, wanted_substance):
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
  
		# Import Logistical Modules (to avoid circular imports)
		from entities import Substance, Significant_Figures
		from precision import Scientific_Handler
  
		# Convert any potential scientific numbers to floats
		given_amount = Scientific_Handler(given_amount).to_float()
  
		answer = 0

		# Convert the given and wanted substances to Substance objects
		given_substance = Substance(f"{self.balanced_dict[given_substance]}{given_substance}")
		wanted_substance = Substance(f"{self.balanced_dict[wanted_substance]}{wanted_substance}")
		if given_measurement == "g":
			self.work_shown.append((f"{Scientific_Handler(given_amount).to_scientific()}{given_measurement} {given_substance.calculation_presentation()} ×"))
		else:
			self.work_shown.append(f"{Scientific_Handler(given_amount).to_scientific()} {given_measurement} {given_substance.calculation_presentation()} ×")
  
		current_measurement = given_measurement # Make a standard variable for the current measurement.
     
		if current_measurement != "mol": # If not in moles, convert to moles.
			given_amount = given_substance.measurement_converter(given_amount, given_measurement, "/", self.work_shown)
			current_measurement = "mol"
	
		# Molar Bridge
		wanted_coefficient = wanted_substance.substance_coefficient()
		given_coefficient = given_substance.substance_coefficient()
		if wanted_coefficient + given_coefficient != 2: # Exclude fractions of 1/1
			self.work_shown.append((f"{wanted_coefficient} {current_measurement} {wanted_substance.calculation_presentation()}", f"{given_coefficient} {current_measurement} {given_substance.calculation_presentation()}"))
			answer = given_amount * (wanted_coefficient / given_coefficient)
		else:
			answer = given_amount

		if wanted_measurement != "mol": # If we're not in moles, convert to the wanted measurement.
			answer = wanted_substance.measurement_converter(answer, wanted_measurement, "*", self.work_shown)
	
		# Round the answer to the given signific3 ant figures
		answer = round(answer, given_significant_figures) # Chemists usually round up, so it's rounded up to the significant figures.
		answer = Significant_Figures().round(answer, given_significant_figures) # Then cut off to the significant figures.

		answer = Scientific_Handler(answer).to_float() # Convert to scientific notation if needed.

		if wanted_measurement == "g":
			self.work_shown.append((f"= {Scientific_Handler(answer).to_scientific()}{wanted_measurement} {wanted_substance.calculation_presentation()}"))
		else:
			self.work_shown.append((f"= {Scientific_Handler(answer).to_scientific()} {wanted_measurement} {wanted_substance.calculation_presentation()}"))
		return f"{Scientific_Handler(answer).to_scientific()} {wanted_measurement} {wanted_substance.calculation_presentation()}", self.work_shown