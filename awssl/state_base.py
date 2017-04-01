class StateBase(object):
	"""
	Base class of all possible States within AWS State Language

	Supported types: "Pass", "Task", "Choice", "Wait", "Succeed", "Fail", "Parallel"

	"""

	def __init__(self, Name=None, Type=None, Comment=""):
		if not Name:
			raise Exception("Name must be specified")
		if not isinstance(Name, str):
			raise Exception("Name must be a string value")
		if not Type:
			raise Exception("Type must be specified (step '{}'".format(Name))
		if not isinstance(Type, str):
			raise Exception("Type must be a string value (step '{}'".format(Name))
		if not Type in ["Pass", "Task", "Choice", "Wait", "Succeed", "Fail", "Parallel"]:
			raise Exception("Type must be one of the allowed types for AWS Step Functions (step '{}'".format(Name))
		self._type = Type
		self._name = Name
		self._comment = ""
		self.set_comment(Comment)

	def validate(self):
		pass

	def to_json(self):
		return {
			"Type" : self.get_type(),
			"Comment" : self.get_comment()
		}

	def get_name(self):
		return self._name

	def get_type(self):
		return self._type

	def get_comment(self):
		return self._comment

	def set_comment(self, Comment=""):
		comment = ""
		if Comment:
			if not isinstance(Comment, str):
				raise Exception("Comment must be a string value if specified, for step ({})".format(self.get_name()))
			comment = Comment
		self._comment = comment

