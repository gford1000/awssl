from .state_input_output import StateInputOutput

class Succeed(StateInputOutput):

	""" 
	Succeed is a state that terminates a State Machine successfully.

	Succeed are typically used as part of a Condition state, and can receive Input and return Output.

	"""

	def __init__(self, Name="", Comment="", InputPath="$", OutputPath="$"):
		super(Succeed, self).__init__(Name=Name, Type="Succeed", Comment=Comment, InputPath=InputPath, OutputPath=OutputPath)

	def validate(self):
		super(Succeed, self).validate()

	def to_json(self):
		return super(Succeed, self).to_json()
