from ..state_base import StateBase
from .state_retry_catch_finally import StateRetryCatchFinally
from ..branch import Branch
from ..parallel_state import Parallel

class ParallelWithFinally(StateRetryCatchFinally):
	"""
	Models the ``ParallelWithFinally`` state, which allows concurrent processing of branches, with the overall state having
	an optional "finally" branch execution after all branches have completed, or when an error is raised that is caught by a ``Catcher``.

	Either:

	* ``EndState`` is ``True`` and ``NextState`` must be ``None``
	* ``EndState`` is ``False`` and ``NextState`` must be a valid instance of a class derived from ``StateBase``.

	Output is returned as a ``list`` of the outputs from each branch.

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
	:param FinallyState: [Optional] First state of the finally branch to be invoked
	:type: FinallyState: Derived from ``StateBase``
	:param BranchList: [Required] ``list`` of ``StateBase`` instances, providing the starting states for each branch to be run concurrently 
	:type: BranchList: list of ``StateBase``

	"""

	def __init__(self, Name=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=None, 
					ResultPath="$", RetryList=None, CatcherList=None, FinallyState=None, BranchList=None):
		"""
		Initializer for the ParallelWithFinally state.

		Either:

		* ``EndState`` is ``True`` and ``NextState`` must be ``None``
		* ``EndState`` is ``False`` and ``NextState`` must be a valid instance of a class derived from ``StateBase``.

		Output is returned as a ``list`` of the outputs from each branch.

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
		:param FinallyState: [Optional] First state of the finally branch to be invoked
		:type: FinallyState: Derived from ``StateBase``
		:param BranchList: [Required] ``list`` of ``StateBase`` instances, providing the starting states for each branch to be run concurrently 
		:type: BranchList: list of ``StateBase``

		"""
		super(ParallelWithFinally, self).__init__(Name=Name, Comment=Comment, 
			InputPath=InputPath, OutputPath=OutputPath, NextState=NextState, EndState=EndState, 
			ResultPath=ResultPath, RetryList=RetryList, CatcherList=CatcherList, FinallyState=FinallyState)
		self._branches = None
		self.set_branch_list(BranchList)

	def _get_underlying_state_no_retry_catch(self, state_name):
		return Parallel(
			Name=state_name,
			BranchList=self.get_branch_list(),
			EndState=True)

	def add_branch(self, StartObject=None):
		"""
		Adds a branch starting at the specified ``StartObject``, which must be inherited from ``StateBase``.
		"""
		if not StartObject:
			raise Exception("StartObject must not be None for a Branch (step '{}'".format(self.get_name()))
		if not isinstance(StartObject, StateBase):
			raise Exception("BranchList must contain only subclasses of StateBase (step '{}'".format(self.get_name()))
		if not self._branches:
			self._branches = []
		self._branches.append(Branch(StartObject))
		self._changed()

	def get_branch_list(self):
		"""
		Returns the list of starting states for each branch.

		:returns: list of ``StateBase``
		"""
		if not self._branches:
			return None
		else:
			return [ b.get_start_state() for b in self._branches ]

	def set_branch_list(self, BranchList=None):
		"""
		Sets the list of starting states for each branch to be executed concurrently.

		At least one branch is required for the state to be valid.

		:param BranchList: [Required] ``list`` of ``StateBase`` instances, providing the starting states for each branch to be run concurrently 
		:type: BranchList: list of ``StateBase``		
		"""		
		if not BranchList:
			self._branches = None
			return

		if not isinstance(BranchList, list):
			raise Exception("BranchList must contain a list of starting states (step '{}'".format(self.get_name()))
		if len(BranchList) == 0:
			raise Exception("BranchList must contain a non-empty list of starting states (step '{}'".format(self.get_name()))
		for o in BranchList:
			if not isinstance(o, StateBase):
				raise Exception("BranchList must contain only subclasses of StateBase (step '{}'".format(self.get_name()))
		self._branches = []
		for o in BranchList:
			self.add_branch(o)				

	def clone(self, NameFormatString="{}"):
		"""
		Returns a clone of this instance, with the clone named per the NameFormatString, to avoid state name clashes.

		If this instance is not an end state, then the next state will also be cloned, to establish a complete clone
		of the branch form this instance onwards.

		:param NameFormatString: [Required] The naming template to be applied to generate the name of the new instance.
		:type NameFormatString: str

		:returns: ``ParallelWithFinally`` -- A new instance of this instance and any other instances in its branch.
		"""
		if not NameFormatString:
			raise Exception("NameFormatString must not be None (step '{}')".format(self.get_name()))
		if not isinstance(NameFormatString, str):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		c = ParallelWithFinally(
			Name=NameFormatString.format(self.get_name()),
			Comment=self.get_comment(),
			InputPath=self.get_input_path(),
			OutputPath=self.get_output_path(),
			EndState=self.get_end_state(),
			ResultPath=self.get_result_path())

		if self.get_retry_list():
			c.set_retry_list(RetryList=[ r.clone() for r in self.get_retry_list() ])

		if self.get_catcher_list():
			c.set_catcher_list(CatcherList=[ catcher.clone(NameFormatString) for catcher in self.get_catcher_list() ])

		if self._branches:
			c.set_branch_list(BranchList=[ b.get_start_state().clone(NameFormatString) for b in self._branches ])

		if self.get_next_state():
			c.set_next_state(NextState=self.get_next_state().clone(NameFormatString))	

		if self.get_finally_state():
			c.set_finally_state(FinallyState=self.get_finally_state().clone(NameFormatString))			

		return c
