from .state_result import StateResult

class Pass(StateResult):
	"""
	Models the Pass state, which can transfer input to output, or can inject specific values via set_result().

	Either:

	* ``EndState`` is ``True`` and ``NextState`` must be ``None``
	* ``EndState`` is ``False`` and ``NextState`` must be a valid instance of a class derived from ``StateBase``.

	Values can be returned by ``Pass`` by specifying a JSON result for ``ResultAsJSON`` such as::

		{
			"output": "This is a value"
		}

	and then using ``OutputPath`` to filter, by specifing `"$.output"`.

	:param Name: [Required] The name of the state within the branch of the state machine
	:type Name: str
	:param Comment: [Optional] A comment describing the intent of this pass state
	:type Comment: str
	:param InputPath: [Optional] Filter on the Input information to be passed to the Pass state.  Default is "$", signifying that all the Input information will be provided
	:type InputPath: str
	:param OutputPath: [Optional] Filter on the Output information to be returned from the Pass state.  Default is "$", signifying that all the result information will be provided
	:type OutputPath: str
	:param EndState: [Optional] Flag indicating if this state terminates a branch of the state machine.  Defaults to ``False``.
	:type EndState: bool
	:param NextState: [Optional] Next state to be invoked within this branch.  Must not be ``None`` unless ``EndState`` is ``True``.
	:type NextState: instance of class derived from ``StateBase``
	:param ResultPath: [Optional] JSONPath indicating where results should be added to the Input.  Defaults to "$", indicating results replace the Input entirely.
	:type ResultPath: str
	:param ResultAsJSON: [Optional] Data to be returned by this state, in JSON format.
	:type ResultPath: dict

	"""

	def __init__(self, Name="", Comment="", InputPath="$", OutputPath="$", EndState=False, NextState=None, ResultPath="$", ResultAsJSON=None):
		"""
		Initialiser for the Pass state.

		:param Name: [Required] The name of the state within the branch of the state machine
		:type Name: str
		:param Comment: [Optional] A comment describing the intent of this pass state
		:type Comment: str
		:param InputPath: [Optional] Filter on the Input information to be passed to the Pass state.  Default is "$", signifying that all the Input information will be provided
		:type InputPath: str
		:param OutputPath: [Optional] Filter on the Output information to be returned from the Pass state.  Default is "$", signifying that all the result information will be provided
		:type OutputPath: str
		:param EndState: [Optional] Flag indicating if this state terminates a branch of the state machine.  Defaults to ``False``.
		:type EndState: bool
		:param NextState: [Optional] Next state to be invoked within this branch.  Must not be ``None`` unless ``EndState`` is ``True``.
		:type NextState: instance of class derived from ``StateBase``
		:param ResultPath: [Optional] JSONPath indicating where results should be added to the Input.  Defaults to "$", indicating results replace the Input entirely.
		:type ResultPath: str
		:param ResultAsJSON: [Optional] Data to be returned by this state, in JSON format.
		:type ResultPath: dict

		"""
		super(Pass, self).__init__(Name=Name, Type="Pass", Comment=Comment, InputPath=InputPath, OutputPath=OutputPath, EndState=EndState, NextState=NextState, ResultPath=ResultPath)
		self._result = None
		self.set_result(ResultAsJSON)

	def validate(self):
		"""
		Validates this instance is correctly specified.

		Raises ``Exception`` with details of the error, if the state machine is incorrectly defined.
		
		"""
		super(Pass, self).validate()

	def to_json(self):
		"""
		Returns the JSON representation of this instance.

		:returns: dict -- The JSON representation
		
		"""
		j = super(Pass, self).to_json()
		if self._result:
			j["Result"] = self.get_result()
		return j

	def get_result(self):
		"""
		Returns the JSON result of this instance.

		:returns: dict -- The JSON representation
		
		"""
		return self._result

	def set_result(self, ResultAsJSON={}):
		"""
		Sets the result to be returned by this instance of ``Pass``.

		:param ResultAsJSON: [Optional] Data to be returned by this state, in JSON format.
		:type ResultPath: dict
		
		"""
		if ResultAsJSON and not isinstance(ResultAsJSON, (dict, list)):
			raise Exception("ResultAsJSON must be valid JSON specification")
		self._result = ResultAsJSON

	def clone(self, NameFormatString="{}"):
		"""
		Returns a clone of this instance, with the clone named per the NameFormatString, to avoid state name clashes.

		If this instance is not an end state, then the next state will also be cloned, to establish a complete clone
		of the branch form this instance onwards.

		:param NameFormatString: [Required] The naming template to be applied to generate the name of the new instance.
		:type NameFormatString: str

		:returns: ``Pass`` -- A new instance of this instance and any other instances in its branch.
		"""
		if not NameFormatString:
			raise Exception("NameFormatString must not be None (step '{}')".format(self.get_name()))
		if not isinstance(NameFormatString, str):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		c = Pass(
			Name=NameFormatString.format(self.get_name()),
			Comment=self.get_comment(),
			InputPath=self.get_input_path(),
			OutputPath=self.get_output_path(),
			EndState=self.get_end_state(),
			ResultPath=self.get_result_path(),
			ResultAsJSON=self.get_result())

		if self.get_next_state():
			c.set_next_state(NextState=self.get_next_state.clone(NameFormatString))	

		return c
