from .state_base import StateBase

class StateInputOutput(StateBase):
	"""
	Base class for States that support InputPath and OutputPath:

		Pass, Task, Choice, Wait, Succeed, Parallel
	"""

	def __init__(self, Name=None, Type=None, Comment="", InputPath="$", OutputPath="$"):
		super(StateInputOutput, self).__init__(Name=Name, Type=Type, Comment=Comment)
		self._input_path = "$"
		self._output_path = "$"
		self.set_input_path(InputPath)
		self.set_output_path(OutputPath)

	def validate(self):
		super(StateInputOutput, self).validate()

	def to_json(self):
		j = super(StateInputOutput, self).to_json()
		j["InputPath"] = self._input_path
		j["OutputPath"] = self._output_path
		return j

	def get_input_path(self):
		return self._input_path

	def set_input_path(self, InputPath="$"):
		if InputPath and not isinstance(InputPath, str):
			raise Exception("InputPath must be either a string value if specified, or None, for step ({})".format(self.get_name()))
		self._input_path = InputPath

	def get_output_path(self):
		return self._output_path

	def set_output_path(self, OutputPath="$"):
		if OutputPath and not isinstance(OutputPath, str):
			raise Exception("OutputPath must be either a string value if specified, or None, for step ({})".format(self.get_name()))
		self._output_path = OutputPath
