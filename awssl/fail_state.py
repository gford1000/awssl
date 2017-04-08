from .state_base import StateBase

class Fail(StateBase):
	"""
	Models the ``Fail`` state, which terminates the state machine with an error code.

	:param Name: [Required] The name of the state within the branch of the state machine
	:type Name: str
	:param Comment: [Optional] A comment describing the intent of this fail state
	:type Comment: str
	:param ErrorName: [Optional] A code to identify the error causing the failed state
	:type ErrorName: str
	:param ErrorCause: [Optional] More detailed information on the cause of the error
	:type ErrorCause: str

	"""

	def __init__(self, Name="", Comment="", ErrorName="", ErrorCause=""):
		"""
		Initialiser for this instance.

		:param Name: [Required] The name of the state within the branch of the state machine
		:type Name: str
		:param Comment: [Optional] A comment describing the intent of this fail state
		:type Comment: str
		:param ErrorName: [Optional] A code to identify the error causing the failed state
		:type ErrorName: str
		:param ErrorCause: [Optional] More detailed information on the cause of the error
		:type ErrorCause: str

		"""
		super(Fail, self).__init__(Name=Name, Type="Fail", Comment=Comment)
		self._error_name = ""
		self._error_cause = ""
		self.set_error_name(ErrorName)
		self.set_error_cause(ErrorCause)

	def validate(self):
		"""
		Validates this instance is correctly specified.

		Raises ``Exception`` with details of the error, if the state machine is incorrectly defined.
		
		"""
		super(Fail, self).validate()

	def to_json(self):
		"""
		Returns the JSON representation of this instance.

		:returns: dict -- The JSON representation
		
		"""
		j = super(Fail, self).to_json()
		j["Error"] = self.get_error_name()
		j["Cause"] = self.get_error_cause()
		return j

	def get_error_name(self):
		"""
		Returns the error name that is associated with this ``Fail`` instance

		:returns: str -- The error name associated with this instance
		"""
		return self._error_name

	def set_error_name(self, ErrorName=""):
		"""
		Set the error name to be associated with this instance.

		:param ErrorName: [Optional] A code to identify the error causing the failed state.
		:type ErrorName: str

		"""
		if not isinstance(ErrorName, str):
			raise Exception("ErrorName must be a valid string")
		self._error_name = ErrorName

	def get_error_cause(self):
		"""
		Returns the more detailed cause of the error that is associated with this instance.

		:returns: str -- The cause of the error associated with this instance
		"""
		return self._error_cause

	def set_error_cause(self, ErrorCause=""):
		"""
		Set the cause of the error associated with this instance.

		:param ErrorCause: [Optional] More detailed information on the cause of the error
		:type ErrorCause: str
		
		"""
		if not isinstance(ErrorCause, str):
			raise Exception("ErrorCause must be a valid string")
		self._error_cause = ErrorCause

