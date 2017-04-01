class Comparison(object):
	"""
	Defines the available set of Comparisons which returns True or False 
	"""

	def __init__(self, Variable=None, Comparator=None, Value=None):
		self._variable = None
		self._comparator = None
		self._comparator_type = None
		self._value = None
		self.set_variable(Variable)
		self.set_comparator(Comparator)
		self.set_value(Value)

	def _get_comparators(self):
		return {
			"String" : ["StringEquals", "StringLessThan", "StringGreaterThan", "StringLessThanEquals", "StringGreaterThanEquals"],
			"Numeric": ["NumericEquals", "NumericLessThan", "NumericGreaterThan", "NumericLessThanEquals", "NumericGreaterThanEquals"],
			"Boolean": ["BooleanEquals"],
			"Timestamp": ["TimestampLessThan", "TimestampGreaterThan", "TimestampLessThanEquals", "TimestampGreaterThanEquals"]
		}

	def _get_value_types(self):
		return {
			"String" : (str),
			"Numeric": (int, float),
			"Boolean": (bool),
			"Timestamp": (str)
		}

	def _validate_value_against_comparator(self, value):
		if not isinstance(value, self._get_value_types()[self._comparator_type]):
			raise Exception("Inconsistent Value provided for ChoiceRule (Comparator: {}, Value: {})".format(self.get_comparator(), Value))

	def get_variable(self):
		return self._variable

	def set_variable(self, Variable=None):
		if (not Variable) or not isinstance(Variable, str):
			raise Exception("ChoiceRule must have a Variable, which must be a string")
		self._variable = Variable

	def get_comparator(self):
		return self._comparator

	def set_comparator(self, Comparator=None):
		if (not Comparator) or not isinstance(Comparator, str):
			raise Exception("ChoiceRule must have a Comparator, which must be a string")
		self._comparator = None
		self._comparator_type = None
		for key in self._get_comparators().keys():			
			if Comparator in self._get_comparators()[key]:
				self._comparator_type = key
				break
		if not self._comparator_type:
			raise Exception("Invalid Comparator provided for ChoiceRule ({})".format(Comparator))
		self._comparator = Comparator

	def get_value(self):
		return self._value

	def set_value(self, Value=None):
		if not Value:
			raise Exception("ChoiceRule must have a Value specified")
		self._validate_value_against_comparator(Value)
		self._value = Value

	def validate(self):
		self._validate_value_against_comparator(self.get_value())

	def to_json(self):
		return {
			"Variable" : self.get_variable(),
			self.get_comparator() : self.get_value()
		}
