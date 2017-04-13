from ..pass_state import Pass 
from ..parallel_state import Parallel
from ..state_base import StateBase
from ..retrier import Retrier

class BranchRetryParallel(Parallel):
	"""
	Extends the Parallel state, providing optional retries on each branch separately.

	Either:

	* ``EndState`` is ``True`` and ``NextState`` must be ``None``
	* ``EndState`` is ``False`` and ``NextState`` must be a valid instance of a class derived from ``StateBase``.

	Output is returned as a ``list`` of the outputs from each branch, as with ``Parallel``.

	:param Name: [Required] The name of the state within the branch of the state machine
	:type Name: str
	:param Comment: [Optional] A comment describing the intent of this pass state
	:type Comment: str
	:param InputPath: [Optional] Filter on the Input information to be passed to the Pass state.  Default is "$", signifying that all the Input information will be provided
	:type InputPath: str
	:param OutputPath: [Optional] Filter on the Output information to be returned from the Pass state.  Default is "$", signifying that all the result information will be provided
	:type OutputPath: str
	:param EndState: [Optional] Flag indicating if this state terminates a branch of the state machine.  Defaults to ``False``
	:type EndState: bool
	:param NextState: [Optional] Next state to be invoked within this branch.  Must not be ``None`` unless ``EndState`` is ``True``
	:type NextState: instance of class derived from ``StateBase``
	:param ResultPath: [Optional] JSONPath indicating where results should be added to the Input.  Defaults to "$", indicating results replace the Input entirely.
	:type ResultPath: str
	:param RetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that cause the entire set of branches to be retried
	:type: RetryList: list of ``Retrier``
	:param CatcherList: [Optional] ``list`` of ``Catcher`` instances corresponding to error states that can be caught and handled by further states being executed in the ``StateMachine``.
	:type: CatcherList: list of ``Catcher``
	:param BranchList: [Required] ``list`` of ``StateBase`` instances, providing the starting states for each branch to be run concurrently 
	:type: BranchList: list of ``StateBase``
	:param BranchRetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that can be retried for each branch
	:type: BranchRetryList: list of ``StateBase``

	"""

	def __init__(self, Name=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=None, 
					ResultPath="$", RetryList=None, CatcherList=None, BranchList=None, BranchRetryList=None):
		super(BranchRetryParallel, self).__init__(Name=Name, Comment=Comment, 
			InputPath=InputPath, OutputPath=OutputPath, NextState=NextState, EndState=EndState, 
			ResultPath=ResultPath, RetryList=RetryList, CatcherList=CatcherList)
		"""
		Initializer for the ``BranchRetryParallel`` state.

		Either:

		* ``EndState`` is ``True`` and ``NextState`` must be ``None``
		* ``EndState`` is ``False`` and ``NextState`` must be a valid instance of a class derived from ``StateBase``.

		:param Name: [Required] The name of the state within the branch of the state machine
		:type Name: str
		:param Comment: [Optional] A comment describing the intent of this pass state
		:type Comment: str
		:param InputPath: [Optional] Filter on the Input information to be passed to the Pass state.  Default is "$", signifying that all the Input information will be provided
		:type InputPath: str
		:param OutputPath: [Optional] Filter on the Output information to be returned from the Pass state.  Default is "$", signifying that all the result information will be provided
		:type OutputPath: str
		:param EndState: [Optional] Flag indicating if this state terminates a branch of the state machine.  Defaults to ``False``
		:type EndState: bool
		:param NextState: [Optional] Next state to be invoked within this branch.  Must not be ``None`` unless ``EndState`` is ``True``
		:type NextState: instance of class derived from ``StateBase``
		:param ResultPath: [Optional] JSONPath indicating where results should be added to the Input.  Defaults to "$", indicating results replace the Input entirely.
		:type ResultPath: str
		:param RetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that cause the entire set of branches to be retried
		:type: RetryList: list of ``Retrier``
		:param CatcherList: [Optional] ``list`` of ``Catcher`` instances corresponding to error states that can be caught and handled by further states being executed in the ``StateMachine``.
		:type: CatcherList: list of ``Catcher``
		:param BranchList: [Required] ``list`` of ``StateBase`` instances, providing the starting states for each branch to be run concurrently 
		:type: BranchList: list of ``StateBase``
		:param BranchRetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that can be retried for each branch
		:type: BranchRetryList: list of ``StateBase``

		"""
		self._branch_list = None
		self._branch_retry_list = None
		self.set_branch_list(BranchList)
		self.set_branch_retry_list(BranchRetryList)

	def _build(self):
		if not self._branch_list:
			return 

		branch_list = []

		if self.get_branch_retry_list() and len(self.get_branch_retry_list()) > 0:
			# Wrap each branch in its own retrying Parallel		
			for b in self._branch_list:
				final_state = Pass(
					Name="{}-Finalizer-{}".format(self.get_name(), b.get_name()),
					Comment="Unpacking of Parallel results from executing '{}'".format(b.get_name()),
					OutputPath="$.[0]",
					EndState=True)

				process_state = Parallel(
					Name="{}-Processor-{}".format(self.get_name(), b.get_name()),
					Comment="Wrapping of branch starting at '{}' in Parallel, to enable Retry".format(b.get_name()),
					EndState=False,
					NextState=final_state,
					BranchList=[b],
					RetryList=self.get_branch_retry_list())

				branch_list.append(process_state)
		else:
			# Do not add in additional Parallel if no Retriers specified, to save costs/time
			branch_list = [ b for b in self.get_branch_list() ]

		super(BranchRetryParallel, self).set_branch_list(branch_list)


	def get_branch_list(self):
		"""
		Returns the list of starting states for each branch to be executed concurrently

		:returns: ``list`` of ``StateBase`` instances
		"""
		return self._branch_list

	def set_branch_list(self, BranchList=None):
		"""
		Sets the list of starting states for each branch to be executed concurrently.

		At least one branch is required for the state to be valid.

		:param BranchList: [Required] ``list`` of ``StateBase`` instances, providing the starting states for each branch to be run concurrently 
		:type: BranchList: list of ``StateBase``		
		"""
		if not BranchList:
			self._branch_list = None
			return

		if not isinstance(BranchList, list):
			raise Exception("BranchList must contain a list of starting states (step '{}')".format(self.get_name()))
		if len(BranchList) == 0:
			raise Exception("BranchList must contain a non-empty list of starting states (step '{}')".format(self.get_name()))
		for o in BranchList:
			if not isinstance(o, StateBase):
				raise Exception("BranchList must contain only subclasses of StateBase (step '{}')".format(self.get_name()))
		self._branch_list = [ b for b in BranchList ]

	def get_branch_retry_list(self):
		"""
		Returns the list of ``Retrier`` instances that will be applied to each branch separately, allowing failure 
		in one branch to be retried without having to re-execute all the branches of the ``Parallel``.

		:returns: ``list`` of ``Retrier`` instances
		"""
		return self._branch_retry_list

	def set_branch_retry_list(self, BranchRetryList=None):
		"""
		Sets the list of ``Retrier`` instance to be applied to the branches in the ``Parallel``.

		If none are set, then the behaviour of this state is equivalent to the ``Parallel`` state.

		:param BranchRetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that can be retried for each branch
		:type: BranchRetryList: list of ``StateBase``

		"""
		if not BranchRetryList:
			self._branch_retry_list = None
			return

		if not isinstance(BranchRetryList, list):
			raise Exception("BranchRetryList must contain a list of Retrier instances (step '{}')".format(self.get_name()))
		if len(BranchRetryList) == 0:
			raise Exception("BranchRetryList must contain a non-empty list of Retrier instances (step '{}')".format(self.get_name()))
		for o in BranchRetryList:
			if not isinstance(o, Retrier):
				raise Exception("BranchRetryList must contain only instances of Retrier - found '{}' (step '{}')".format(type(o), self.get_name()))
		self._branch_retry_list = [ r for r in BranchRetryList ]

	def validate(self):
		"""
		Validates this instance is correctly specified.

		Raises ``Exception`` with details of the error, if the state machine is incorrectly defined.
		
		"""
		self._build()
		super(BranchRetryParallel, self).validate()

	def to_json(self):
		"""
		Returns the JSON representation of this instance.

		:returns: dict -- The JSON representation
		
		"""
		self._build()
		return super(BranchRetryParallel, self).to_json()

	def clone(self, NameFormatString="{}"):
		"""
		Returns a clone of this instance, with the clone named per the NameFormatString, to avoid state name clashes.

		If this instance is not an end state, then the next state will also be cloned, to establish a complete clone
		of the branch form this instance onwards.

		:param NameFormatString: [Required] The naming template to be applied to generate the name of the new instance.
		:type NameFormatString: str

		:returns: ``BranchRetryParallel`` -- A new instance of this instance and any other instances in its branch.
		"""
		if not NameFormatString:
			raise Exception("NameFormatString must not be None (step '{}')".format(self.get_name()))
		if not isinstance(NameFormatString, str):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		c = BranchRetryParallel(
			Name=NameFormatString.format(self.get_name()),
			Comment=self.get_comment(),
			InputPath=self.get_input_path(),
			OutputPath=self.get_output_path(),
			EndState=self.get_end_state(),
			ResultPath=self.get_result_path())

		if self.get_branch_list():
			c.set_branch_list(BranchList=[ b.clone(NameFormatString) for b in self.get_branch_list() ])

		if self.get_branch_retry_list():
			c.set_branch_retry_list(BranchRetryList=[ r.clone() for r in self.get_branch_retry_list() ])

		if self.get_next_state():
			c.set_next_state(NextState=self.get_next_state.clone(NameFormatString))	

		return c
