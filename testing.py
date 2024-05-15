#
# Nathan Parker | 5/12/24 | v0.8.0
# It's important to test inputs, and this file does just that. 
# With 60 tests, it checks various methods and sets of methods 
# to ensure data can be inputted and processed correctly. 
# Each class is tested in some way (except the GUI — it has its own error detections),
# and in writing this file brought up key errors that were fixed before pushing into submission! 
#
# Note: These don't contain docstrings, as they're just tests, and the
# name / section comments explain what they're testing.
#
# Main Libraries:
# - unittest (Testing)

# Testing Library
import unittest

# Logical Libraries
from entities import Substance, Equation
from precision import Scientific_Handler, Significant_Figures

class Test_Substances(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.water = Substance("H2O")
		self.two_waters = Substance("2H2O")
		self.many_waters = Substance("32H2O")
		self.garbage = Substance("0sPyD3r") # Sorry Ben! - VSC Gang
		self.complex = Substance("K4[Fe(SCN)6]")
		self.diflorine = Substance("F2")
		self.ammonium_chloride = Substance("NH4Cl")
		self.sulfur = Substance("S")
		self.oxygen_dichloride = Substance("OCl2")

	# Testing Instance
	def test_substance_instance(self):
		self.assertIsInstance(self.water, Substance)

	#
	# Testing Substance Coefficients Handling
	#

	def test_get_coefficient_with_no_coefficient(self):
		self.assertEqual(self.water.substance_coefficient(), 1)

	def test_get_coefficient_with_coefficient(self):
		self.assertEqual(self.two_waters.substance_coefficient(), 2)

	def test_get_multiple_coefficient(self):
		self.assertEqual(self.many_waters.substance_coefficient(), 32)

	def test_remove_coefficient(self):
		self.assertEqual(self.two_waters.remove_coefficients(), "H2O")

	def test_remove_coefficients(self):
		self.assertEqual(self.many_waters.remove_coefficients(), "H2O")

	#
	# Testing Substance Subscripts Handling
	#

	def test_add_subscript(self):
		self.assertEqual(self.water.add_subscripts(), "H₂O")

	def test_add_subscripts(self):
		substance = Substance("(H2O2)3")
		self.assertEqual(substance.add_subscripts(), "(H₂O₂)₃")

	def test_replace_subscript(self):
		substance = Substance("H₂O")
		self.assertEqual(substance.replace_subscripts(), "H2O")

	def test_replace_subscripts(self):
		substance = Substance("(H₂O₂)₃")
		self.assertEqual(substance.replace_subscripts(), "(H2O2)3")

	def test_calculation_presentation(self):
		self.assertEqual(self.water.calculation_presentation(), "H₂O")
  
	def test_calculation_presentation_with_coefficient(self):
		self.assertEqual(self.two_waters.calculation_presentation(), "H₂O")

	#
	# Testing Substance Element Scanning
	#

	def test_unique_element_scans(self):
		self.assertEqual(self.water.element_scanner("unique"), ["H", "O"])

	def test_raw_element_scans(self):
		self.assertEqual(self.water.element_scanner("raw"), ["H", "-", "O"])

	def test_raw_complex_element_scans(self):
		self.assertEqual(self.complex.element_scanner("raw"), ['K', '-', 'Fe', 'S', 'C', 'N', '-'])

	def test_invalid_element_scans(self):
		with self.assertRaises(Exception):
			self.garbage.element_scanner("unique")
   
	def test_substance_scanner_water(self):
		self.assertEqual(self.water.substance_scanner(), [('H', (1, 2, 1)), ('O', (1, 1, 1))])

	def test_substance_scanner_two_waters(self):
		self.assertEqual(self.two_waters.substance_scanner(), [('H', (1, 2, 1)), ('O', (1, 1, 1))])

	#
	# Testing Substance Scanner Handling
	#

	def test_substance_scanner_garbage(self):
		with self.assertRaises(Exception): # Element(s) not found
			self.garbage.substance_scanner()

	def test_substance_scanner_complex(self):
		self.assertEqual(self.complex.substance_scanner(), [('K', (1, 4, 1)), ('Fe', (1, 1, 1)), ('S', (1, 1, 6)), ('C', (1, 1, 6)), ('N', (1, 1, 6))])

	#
	# Testing Substance Measurement Conversions
	#

	def test_measurement_converter_grams_multiplication(self):
		self.assertEqual(self.water.measurement_converter(1, "g", "*", []), 18.015)
  
	def test_measurement_converter_grams_division(self):
		self.assertEqual(self.water.measurement_converter(1, "g", "/", []), 0.055509297807382736)

	def test_measurement_converter_liters_multiplication(self):
		self.assertEqual(self.water.measurement_converter(1, "L", "*", []), 22.4)

	def test_measurement_converter_liters_division(self):
		self.assertEqual(self.water.measurement_converter(1, "L", "/", []), 0.044642857142857144)
  
	def test_measurement_converter_representative_particles_multiplication(self):
		self.assertEqual(self.water.measurement_converter(1, "r.p.", "*", []), 6.02e23)
  
	def test_measurement_converter_representative_particles_division(self):
		self.assertEqual(self.water.measurement_converter(1, "r.p.", "/", []), 1.6611295681063124e-24)

	#
	# Testing Substance Calculations
	#

	def test_stoichify_diflorine(self):
		self.assertEqual(self.diflorine.stoichify("9.3021 x 10^27", 5, "r.p.", "F2", "g", "F2")[0], "587,110 g F₂")

	def test_stoichify_sulfur(self):
		self.assertEqual(self.sulfur.stoichify(4.2, 2, "mol", "S", "g", "S")[0], "130 g S")

	def test_stoichify_oxygen_dichloride(self):
		self.assertEqual(self.oxygen_dichloride.stoichify(392.1, 4, "g", "OCl2", "r.p.", "OCl2")[0], "2.716 × 10²⁴ r.p. OCl₂")

	def test_stoichify_ammonium_chloride(self):
		self.assertEqual(self.ammonium_chloride.stoichify("3.902 x 10^28", 4, "r.p.", "NH4Cl", "g", "NH4Cl")[0], "3.467 × 10⁶ g NH₄Cl")

class Test_Equations(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.first = Equation("SO2 + O2 -> SO3")
		self.second = Equation("C3H8 + O2 -> CO2 + H2O")
		self.third = Equation("Al + Cl2 -> AlCl3")
		self.insane = Equation("K4[Fe(SCN)6] + K2Cr2O7 + H2SO4 → Fe2(SO4)3 + Cr2(SO4)3 + CO2 + H2O + K2SO4 + KNO3")

	def test_equation_instance(self):
		self.assertIsInstance(self.first, Equation)

	#
	# Testing Equation Type Checking (includes charges, states, concatenation, and arrow replacements)
	#

	def test_equation_type_checker_arrow_states(self):
		equation = Equation("SO2(g) + O2(g) -> SO3(g)")
		self.assertEqual(equation.type_checker(), "SO2(g) + O2(g) → SO3(g)")

	def test_equation_type_checker_concat(self):
		with self.assertRaises(Exception): # Improper concatenation
			equation = Equation("SO2(g) + -> SO3(g)").type_checker()

	def test_equation_type_checker_oxidation_reduction(self):
		equation = Equation("SO2(g) + O2-(g) -> SO3(g)")
		with self.assertRaises(Exception): # Includes a charge
			equation.type_checker()		

	#
	# Testing Equation Balancing
 	# 	Includes type-checking, element scanning, substance scanning, matrix building/solving, and
	# 	also the final balanced equation.
	#
 
	def test_equation_balancer_first(self):
		self.assertEqual(self.first.balanced, "2SO₂ + 1O₂ → 2SO₃")
  
	def test_equation_balancer_second(self):
		self.assertEqual(self.second.balanced, "1C₃H₈ + 5O₂ → 3CO₂ + 4H₂O")
  
	def test_equation_balancer_third(self):
		self.assertEqual(self.third.balanced, "2Al + 3Cl₂ → 2AlCl₃")
  
	def test_equation_balancer_insane(self):
		self.assertEqual(self.insane.balanced, "6K₄[Fe(SCN)₆] + 97K₂Cr₂O₇ + 355H₂SO₄ → 3Fe₂(SO₄)₃ + 97Cr₂(SO₄)₃ + 36CO₂ + 355H₂O + 91K₂SO₄ + 36KNO₃")

	def test_equation_balancer_garbage(self):
		with self.assertRaises(Exception): # Element(s) not found
			equation = Equation("H2O + 2 -> H2O")

	#
	# Testing Equation Stoichification ( :D )
	# 	Includes the whole stoichiometry.py class of Stoichify, in which
	#   stoichiometry calculations are performed, with all given and wanted parameters,
	#   to convert the given substance to the wanted substance. While also reporting all
	#   number in the correct significant figures, to ensure the maximum precision and accuracy.
	#

	# Simple multiplication
	def test_equation_stoichify_first(self):
		self.assertEqual(self.first.stoichify(3.4, 2, "mol", "SO2", "mol", "SO3")[0], "3.4 mol SO₃")

	# Simple division
	def test_equation_stoichify_first_division(self):
		self.assertEqual(self.first.stoichify(4.7, 2, "mol", "SO2", "mol", "O2")[0], "2.4 mol O₂")

	# Multi-stepped multiplication + conversion
	def test_equation_stoichify_second_(self):
		self.assertEqual(self.second.stoichify(2.8, 2, "mol", "C3H8", "g", "CO2")[0], "370 g CO₂")

	# Another multi-stepped multiplication + conversion
	def test_equation_stoichify_second_another_one(self):
		self.assertEqual(self.second.stoichify(3.8, 2, "mol", "C3H8", "g", "O2")[0], "610 g O₂")

	# Multi-stepped division + conversion
	def test_equation_stoichify_second_division(self):
		self.assertEqual(self.second.stoichify(25, 2, "g", "C3H8", "mol", "H2O")[0], "2.3 mol H₂O")

	# Complex multi-stepped multiplication + division + conversion (four fractions)
	def test_equation_stoichify_third(self):
		self.assertEqual(self.third.stoichify(35, 2, "g", "Al", "g", "AlCl3")[0], "170 g AlCl₃")

	# Another complex multi-stepped multiplication + division + conversion (four fractions)
	def test_equation_stoichify_third_another_one(self):
		self.assertEqual(self.third.stoichify(42.8, 2, "g", "Al", "g", "Cl2")[0], "170 g Cl₂")

class Test_Precision(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.regular_scientific = Scientific_Handler("9.3021 x 10^27")
		self.shorthand_scientific = Scientific_Handler("9.3021e27")
		self.large_integer = Scientific_Handler("1500000000000000000")
		self.small_float = Scientific_Handler(1.23e-10)
		self.bigger_small_float = Scientific_Handler(1.23e-2)

	# Testing Instance
	def test_scientific_handler_instance(self):
		self.assertIsInstance(self.regular_scientific, Scientific_Handler)

	#
	# Testing Scientific Notation Conversions / Floatation
	#

	def test_large_int_to_scientific(self):
		self.assertEqual(self.large_integer.to_scientific(), "1.500 × 10¹⁸")

	def test_small_float_to_scientific(self):
		self.assertEqual(self.small_float.to_scientific(), "1.23 × 10⁻¹⁰")

	def test_small_float_to_float(self):
		self.assertEqual(self.bigger_small_float.to_float(), 0.0123)

	def test_alt_scientific_format(self):
		self.alt = Scientific_Handler("9.3021 * 10^27")
		self.assertEqual(self.shorthand_scientific.to_scientific(), "9.3021 × 10²⁷")

	def test_other_alt_scientific_format(self):
		self.alt = Scientific_Handler("9.3021e27")
		self.assertEqual(self.alt.to_scientific(), "9.3021 × 10²⁷")

	def test_other_alt_capital_scientific_format(self):
		self.alt = Scientific_Handler("9.3021E27")
		self.assertEqual(self.alt.to_scientific(), "9.3021 × 10²⁷")

	def test_negative_scientific(self):
		self.negative = Scientific_Handler("9.3021e-27")
		self.assertEqual(self.negative.to_scientific(), "9.3021 × 10⁻²⁷")

	#
	# Testing Significant Figures Calculations
	#

	# Small ints like 25, 100, 5487, etc.
	def test_sig_figs_parser(self):
		self.assertEqual(Significant_Figures().parser(25), 2)

	# Bigger ints like 150000000, 3000000, etc.
	def test_sig_figs_parser_big_int(self):
		self.assertEqual(Significant_Figures().parser(150000000), 2)

	# Significant figures in scientific notation
	def test_sig_figs_scientific(self):
		self.assertEqual(Significant_Figures().parser("9.3021 x 10^27"), 5)

	# Leading and trailing zeros
	def test_another_sig_fig_scientific(self):
		self.assertEqual(Significant_Figures().parser(0000003.4000000), 2)

	def test_inbetween_zero_sig_fig_scientific(self):
		self.assertEqual(Significant_Figures().parser(00003.4010000), 4)

	# In-between zeros
	def test_crazy_sig_figs(self):
		self.assertEqual(Significant_Figures().parser(90845375987.0003), 15)

#
# Fixes made along the way
#   However, I did testing last, which was a big mistake. I made dozens 
# 	of errors in the code, fixed along the way. GitHub commits show the
# 	progression of the code, and the final product is a lot more robust
# 	than the initial code. Next time, I'll test each method upon creation.
#

# Had to fix with returning a calculation presentation, wasn't returning a string
# Rearrange checks in the type_checker to prevent unforeseen format slips (like including states)  
# Made sure to include proper subscripting and superscripting in the asserting equals. 
# Handle the re.sub for the scientific notation to include proper typing.
# Had to add lower() to cover capital E in scientific notation.

if __name__ == "__main__":
    unittest.main()