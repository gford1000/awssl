from .state_result import StateResult

class Pass(StateResult):
	"""
	Models the Pass state, which can transfer input to output, or can inject specific values via set_result()
	"""

	def __init__(self, Name="", Comment="", InputPath="$", OutputPath="$", EndState=False, NextState=None, ResultPath="$", ResultAsJSON=None):
		super(Pass, self).__init__(Name=Name, Type="Pass", Comment=Comment, InputPath=InputPath, OutputPath=OutputPath, EndState=EndState, NextState=NextState, ResultPath=ResultPath)
		self._result = None
		self.set_result(ResultAsJSON)

	def validate(self):
		super(Pass, self).validate()

	def to_json(self):
		j = super(Pass, self).to_json()
		if self._result:
			j["Result"] = self.get_result()
		return j

	def get_result(self):
		return self._result

	def set_result(self, ResultAsJSON={}):
		if ResultAsJSON and not isinstance(ResultAsJSON, dict):
			raise Exception("ResultAsJSON must be valid JSON specification")
		self._result = ResultAsJSON
