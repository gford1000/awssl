from .branch import Branch
from json import dumps

class StateMachine(object):
	"""
	StateMachine will execute the main branch, starting from the state specified by ``StartState``.

	The ASL JSON can be returned by calling ``print``.

	:param Comment: [Optiona] A comment describing the processing of the state machine
	:type Comment: str
	:param ASLVersion: [Optional] The version of the ASL specification.  Only 1.0 is currently supported
	:type ASLVersion: str
	:param StartState: [Required] The starting state for the start machine.  Must not be ``None``
	:type StartState: any start class derived from ``StateBase``
	:param TimeoutSeconds: [Optional] The maximum number of seconds the state machine is allowed to run
	:type TimeoutSeconds: int

	"""

	def __init__(self, Comment="", ASLVersion="1.0", StartState=None, TimeoutSeconds=None):
		"""
		StateMachine that constructs the ASL compliant JSON by typing ``print``.

		:param Comment: [[Optional]] A description of the processing of the state machine
		:type Comment: str
		:param ASLVersion: [[Optional]] The version of the ASL specification.  Only 1.0 is currently supported
		:type ASLVersion: str
		:param StartState: [[Required]] The starting state for the start machine.  Must not be ``None``
		:type StartState: any start class derived from ``StateBase``
		:param TimeoutSeconds: [Optional] The maximum number of seconds the state machine is allowed to run
		:type TimeoutSeconds: int

		"""
		self._comment = ""
		self._asl_version = ""
		self._branch = None
		self._timeout_seconds = None
		self.set_comment(Comment)
		self.set_asl_version(ASLVersion)
		self.set_start_state(StartState)
		self.set_timeout_seconds(TimeoutSeconds)

	def get_start_state(self):
		"""
		Returns the object representing the starting state for the state machine.

		:returns: ``StateBase`` -- A state class derived from ``StateBase``

		"""
		return self._branch.get_start_state()

	def set_start_state(self, StartState=None):
		"""
		Sets the starting state for the state machine.

		:param StartState: [[Required]] The starting state for the start machine.  Must not be ``None``
		:type StartState: any start class derived from ``StateBase``

		"""
		self._branch = Branch(StartState)

	def get_comment(self):
		"""
		Returns the comment describing the state machine.

		:returns: str -- The comment associated with the state machine

		"""
		return self._comment

	def set_comment(self, Comment=""):
		"""
		Sets the comment describing the state machine.

		:param Comment: [[Optional]] A description of the processing of the state machine
		:type Comment: str

		"""
		if not Comment:
			Comment = ""
		self._comment = Comment

	def get_asl_version(self):
		"""
		Returns the ASL version specification used for the state machine definition.

		:returns: str -- The version of ASL being used

		"""
		return self._asl_version

	def set_asl_version(self, ASLVersion="1.0"):
		"""
		Sets the ASL version specification being used for the state machine definition.

		:param ASLVersion: [[Optional]] The version of the ASL specification.  Only 1.0 is currently supported
		:type ASLVersion: str

		"""
		if not ASLVersion:
			ASLVersion = "1.0"
		if ASLVersion != "1.0":
			raise Exception("Only version 1.0 of ASL is supported")
		self._asl_version = ASLVersion

	def get_timeout_seconds(self):
		"""
		Returns the maximum number of seconds the state machine is allowed to run.

		:returns: int -- the maximum number of seconds allowed

		"""
		return self._timeout_seconds

	def set_timeout_seconds(self, TimeoutSeconds):
		"""
		Sets the maximum number of seconds the state machine is allowed to run.

		:param TimeoutSeconds: [[Optional]] The maximum number of seconds the state machine is allowed to run.
		:type TimeoutSeconds: int

		"""
		if not isinstance(TimeoutSeconds, int):
			raise Exception("TimeoutSeconds must be an int")
		self._timeout_seconds = TimeoutSeconds

	def __str__(self):
		self.validate()

		j = self._branch.to_json()
		j["Comment"] = self.get_comment()
		j["Version"] = self.get_asl_version()
		if self.get_timeout_seconds() is not None:
			j["TimeoutSeconds"] = self.get_timeout_seconds()

		return dumps(j, sort_keys=True, indent=4)

	def validate(self):
		"""
		Validates the state machine is correctly specified, compared to the version of the ASL being used.

		Raises ``Exception`` with details of the error, if the state machine is incorrectly defined.

		"""
		if not self._branch:
			raise Exception("StartState must be specified for the StateMachine")

		self._branch.validate()
