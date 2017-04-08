from .state_base import StateBase

class Fail(StateBase):

	def __init__(self, Name="", Comment="", ErrorName="", ErrorCause=""):
		super(Fail, self).__init__(Name=Name, Type="Fail", Comment=Comment)
		self._error_name = ""
		self._error_cause = ""
		self.set_error_name(ErrorName)
		self.set_error_cause(ErrorCause)

	def validate(self):
		super(Fail, self).validate()

	def to_json(self):
		j = super(Fail, self).to_json()
		j["Error"] = self.get_error_name()
		j["Cause"] = self.get_error_cause()
		return j

	def get_error_name(self):
		return self._error_name

	def set_error_name(self, ErrorName=""):
		if not isinstance(ErrorName, str):
			raise Exception("ErrorName must be a valid string")
		self._error_name = ErrorName

	def get_error_cause(self):
		return self._error_cause

	def set_error_cause(self, ErrorCause=""):
		if not isinstance(ErrorCause, str):
			raise Exception("ErrorCause must be a valid string")
		self._error_cause = ErrorCause

