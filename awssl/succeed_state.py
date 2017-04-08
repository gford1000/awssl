from .state_input_output import StateInputOutput

class Succeed(StateInputOutput):
	""" 
	Succeed is a state that terminates a State Machine successfully.

	Succeed are typically used as part of a Condition state, and can receive Input and return Output.

	:param Name: [Required] The name of the state within the branch of the state machine
	:type Name: str
	:param Comment: [Optional] A comment describing the intent of this pass state
	:type Comment: str
	:param InputPath: [Optional] Filter on the Input information to be passed to the Pass state.  Default is "$", signifying that all the Input information will be provided
	:type InputPath: str
	:param OutputPath: [Optional] Filter on the Output information to be returned from the Pass state.  Default is "$", signifying that all the result information will be provided
	:type OutputPath: str

	"""

	def __init__(self, Name="", Comment="", InputPath="$", OutputPath="$"):
		""" 
		Initialiser for an instance of Succeed.

		:param Name: [Required] The name of the state within the branch of the state machine
		:type Name: str
		:param Comment: [Optional] A comment describing the intent of this pass state
		:type Comment: str
		:param InputPath: [Optional] Filter on the Input information to be passed to the Pass state.  Default is "$", signifying that all the Input information will be provided
		:type InputPath: str
		:param OutputPath: [Optional] Filter on the Output information to be returned from the Pass state.  Default is "$", signifying that all the result information will be provided
		:type OutputPath: str

		"""
		super(Succeed, self).__init__(Name=Name, Type="Succeed", Comment=Comment, InputPath=InputPath, OutputPath=OutputPath)

	def validate(self):
		"""
		Validates this instance is correctly specified.

		Raises ``Exception`` with details of the error, if the state machine is incorrectly defined.
		
		"""
		super(Succeed, self).validate()

	def to_json(self):
		"""
		Returns the JSON representation of this instance.

		:returns: dict -- The JSON representation
		
		"""
		return super(Succeed, self).to_json()
