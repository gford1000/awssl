from .state_next_end import StateNextEnd

class StateResult(StateNextEnd):
	"""
	Base class for States that support ResultPaths

		Pass, Task, Parallel
	"""

	def __init__(self, Name=None, Type=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=None, ResultPath="$"):
		super(StateResult, self).__init__(Name=Name, Type=Type, Comment=Comment, InputPath=InputPath, OutputPath=OutputPath, NextState=NextState, EndState=EndState)
		self._result_path = "$"
		self.set_result_path(ResultPath)

	def validate(self):
		super(StateResult, self).validate()

	def to_json(self):
		j = super(StateResult, self).to_json()
		j["ResultPath"] = self.get_result_path()
		return j

	def get_result_path(self):
		return self._result_path

	def set_result_path(self, ResultPath="$"):
		if ResultPath and not isinstance(ResultPath, str):
			raise Exception("ResultPath must be either a string value if specified, or None, for step ({})".format(self.get_name()))
		self._result_path = ResultPath
