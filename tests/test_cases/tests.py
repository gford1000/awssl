import imp
import os
import os.path

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def get_tests(Directory="."):
	"""
	Returns a list of tests that can be executed, by test file name.

	Each list item is of the form:

	{
		"File": "Name of file containing tests",
		"Tests": [
			{
				"Name": "Name of the test",
				"Func": "Function to generate the test result",
				"ResultFileName": "Relative file name of the test result"
			},
			...
		]
	}

	"""

	def get_files():
		# Get list of python scripts in current directory
		files = [ os.path.splitext(f)[0] for f in os.listdir(".") if f.endswith(".py")]
		files.remove("__init__")
		files.remove("tests")
		return files

	def import_registry_func(file_name, registry_function_list):
		# Attempt to import the specified file and add its registry_function_list, if it exists
		REGISTRY_FUNC = "register_tests"
		flib = None
		try:
			flib = imp.load_source("{}.{}".format(file_name, REGISTRY_FUNC), "./{}.py".format(file_name))
			registry_function_list.append({"File":file_name, "Func":getattr(flib, REGISTRY_FUNC)})
		except Exception as e:
			print "Error loading '{}': {}".format(file_name, e)

	def create_registry_function_list():
		# Compile the set of registry functions
		registry_function_list = []
		for file in get_files():
			import_registry_func(file, registry_function_list)
		return registry_function_list

	def validate_test_data(d):
		if d == None:
			raise Exception("None returned")
		if not isinstance(d, list):
			raise Exception("A list must be returned")
		for o in d:
			if not isinstance(o, dict):
				raise Exception("The returned list must contain only dict objects")
			for a in ["Name", "Func", "ResultFileName"]:
				if not o.get(a, None):
					raise Exception("The return list of test details contains an object missing attribute '{}'".format(a))

	# Retrieve fully expanded directory
	directory = os.path.abspath(Directory)

	registry = []
	with cd(directory):
		# Retrieve tests within the specified directory
		for f in create_registry_function_list():
			try:
				test_list = f["Func"]()
				registry.append(
					{
						"File": f["File"],
						"Tests": test_list
					})
			except Exception as e:
				print "Error processing test registration of '{}': {}".format(f["File"], e)

		return registry
