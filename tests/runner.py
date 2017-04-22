# Allow awssl and awssl.ext to be found by tests
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Access point to the set of tests defined in ./test_cases
from test_cases import get_tests

_VERBOSE = True

def run_tests():
	"""
	Entry point to test processing
	"""

	def print_msg(msg, Override=False):
		"""
		Controls level of reporting
		"""
		if _VERBOSE or Override:
			print msg

	def execute():
		"""
		Runs all tests
		"""

		def run_tests_for_module(module_tests):
			"""
			Execute all the tests registered in the specified module
			"""

			def run_test(test):
				"""
				Execute a single test, comparing it to the correct result by string comparison
				"""

				def get_expected_result(test):
					"""
					Retrieve the results for the test from its result file
					"""
					try:
						with open(test["ResultFileName"], "r") as f:
							return f.read()
					except Exception as e:
						raise Exception("Unable to read results file '{}' for test '{}': {}".format(test["ResultFileName"], test["Name"], e))

				print_msg("\t\tRunning test '{}'".format(test["Name"]))

				expected_result = ""
				try:
					expected_result = get_expected_result(test)
				except Exception as e:
					return (0, 1, e)

				actual_result = ""
				try:
					actual_result = str(test["Func"]())
				except Exception as e:
					actual_result = str(e)

				if actual_result == expected_result:
					return (1, 0, None)
				else:
					return (0, 1, "{}:\nExpected:\n---\n{}\n---\nActual:\n---\n{}\n---".format(test["Name"], expected_result, actual_result))


			print_msg("\tRunning tests in module '{}'".format(module_tests["File"]))
			results = { "File": module_tests["File"], "Passed": 0, "Failed": 0, "Errors": [] }
			for test in module_tests["Tests"]:
				p, f, i = run_test(test)
				results["Passed"] = results["Passed"] + p 
				results["Failed"] = results["Failed"] + f
				if i:
					results["Errors"].append(i)
			return results

		results = { "Passed": 0, "Failed": 0, "Errors": [] }
		for tests in get_tests("./test_cases"):
			module_results = run_tests_for_module(tests)
			results["Passed"] = results["Passed"] + module_results["Passed"] 
			results["Failed"] = results["Failed"] + module_results["Failed"]
			if module_results["Errors"]:
				results["Errors"].append(module_results)
		return results

	print_msg("Running tests...")
	results = execute()
	print_msg("Tests completed.\n")
	if results["Failed"] == 0:
		print_msg("All tests passed", Override=True)
	else:
		print_msg("Failed {} of {}.".format(results["Failed"], results["Passed"] + results["Failed"]), Override=True)
		print_msg("\nDetails:")
		for d in results["Errors"]:
			print_msg("\t Module '{}':".format(d["File"]))
			for e in d["Errors"]:
				print_msg("\t\t{}".format(e))


if __name__ == "__main__":
	run_tests()
