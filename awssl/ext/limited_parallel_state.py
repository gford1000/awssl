from ..pass_state import Pass 
from ..task_state import Task 
from ..parallel_state import Parallel
from ..retrier import Retrier
from ..state_base import StateBase
from ..state_retry_catch import StateRetryCatch
from .for_state import For, get_ext_arn, _INITIALIZER, _LIMITED_PARALLEL_CONSOLIDATOR

class LimitedParallel(StateRetryCatch):
	"""
	Limited Parallel allows a throttled amount of concurrent processing, constrained by the value of ``MaxConcurrent``.

	Each branch executed is the same, starting at ``BranchState``, and the number of branch executions is specified by ``Iterations``.

	The value of the iterator is passed to each branch, so that ``Task``s in the branch can process appropriately.  The location of the
	iterator is specified by ``IteratorPath``.

	Branch executions have optional ``Retrier`` lists, which allow individual executions to be retried.  In addition, the state also
	supports retries and catches, but this will result in all branches being re-executed.

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
	:param BranchState: [Required] ``StateBase`` instance, providing the starting state for each branch to be run concurrently 
	:type: BranchState: ``StateBase``
	:param BranchRetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that cause the ``For`` loop iteration to be retried.  This will occur until the number of retries has been exhausted for this iteration, afterwhich state level ``Retrier`` will be triggered if specified
	:type BranchRetryList: list of ``Retrier``
	:param: Iterations: [Required] The total number of branches to be executed.  Must be larger than zero
	:type: Iterations: int
	:param: MaxConcurrency: [Required] The maximum number of branches that are to executed concurrently.  Must be larger than zero
	:type: MaxConcurrency: int
	:param: IteratorPath: [Required] The JSONPath in which to inject the iterator value into the Input passed to the branch
	:type: IteratorPath: str

	"""

	def __init__(self, Name=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=None, 
					ResultPath="$", RetryList=None, CatcherList=None, 
					BranchState=None, BranchRetryList=None,
					Iterations=0, MaxConcurrency=1, IteratorPath="$.iteration"):
		"""
		Initializer Limited Parallel allows a throttled amount of concurrent processing, constrained by the value of ``MaxConcurrent``.

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
		:param BranchState: [Required] ``StateBase`` instance, providing the starting state for each branch to be run concurrently 
		:type: BranchState: ``StateBase``
		:param BranchRetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that cause the ``For`` loop iteration to be retried.  This will occur until the number of retries has been exhausted for this iteration, afterwhich state level ``Retrier`` will be triggered if specified
		:type BranchRetryList: list of ``Retrier``
		:param: Iterations: [Required] The total number of branches to be executed.  Must be larger than zero
		:type: Iterations: int
		:param: MaxConcurrency: [Required] The maximum number of branches that are to executed concurrently.  Must be larger than zero
		:type: MaxConcurrency: int
		:param: IteratorPath: [Required] The JSONPath in which to inject the iterator value into the Input passed to the branch
		:type: IteratorPath: str

		"""
		super(LimitedParallel, self).__init__(Name=Name, Type="Ext", Comment=Comment, 
			InputPath=InputPath, OutputPath=OutputPath, NextState=NextState, EndState=EndState, 
			ResultPath=ResultPath, RetryList=RetryList, CatcherList=CatcherList)
		self._branch_state = None
		self._max_concurrent = 1
		self._iterator_path = None
		self._iterations = 0
		self._lp_branch_retry_list = None
		self.set_branch_state(BranchState)
		self.set_max_concurrency(MaxConcurrency)
		self.set_iterator_path(IteratorPath)
		self.set_iterations(Iterations)
		self.set_branch_retry_list(BranchRetryList)

	def _lp_build(self):
		"""
		This does the heavy lifting of declaring the LimitedParallel loop
		"""

		def create_states_for_cycle(cycle, iterations, iteration_offset, branch_state, branch_retry_list, iterator_path, prior_state, state_name):

			for_state = For(Name="{}-For-{}".format(state_name, cycle),
							EndState=True,
							From=iteration_offset, 
							To=iteration_offset+iterations, 
							Step=1, 
							BranchState=branch_state,
							BranchRetryList=branch_retry_list,
							IteratorPath=iterator_path, 
							ParallelIteration=True)

			inputs = Pass(Name="{}-Pass-Inputs-{}".format(state_name, cycle), 
				OutputPath="$.[0]",
				EndState=True)

			existing_results = Pass(Name="{}-Pass-Results-{}".format(state_name, cycle), 
				OutputPath="$.[1]",
				EndState=True)

			loop_inputs = Pass(Name="{}-Loop-Inputs-{}".format(state_name, cycle), 
				OutputPath="$.[0]",
				EndState=False,
				NextState=for_state)

			branch_list = [ inputs, existing_results, loop_inputs]

			initializer_arn = get_ext_arn(_LIMITED_PARALLEL_CONSOLIDATOR)
			if cycle == 0:
				initializer_arn = get_ext_arn(_INITIALIZER)

			cycle_state = Parallel(Name="{}-Parallel-{}".format(state_name, cycle), 
									EndState=True,
									BranchList=branch_list)

			initializer = Task(Name="{}-Initializer-{}".format(state_name, cycle),
							ResourceArn=initializer_arn,
							EndState=False,
							NextState=cycle_state)

			if prior_state:
				prior_state.set_end_state(False)
				prior_state.set_next_state(initializer)

			return (initializer, cycle_state)

		initial_state = None
		prior_state = None
		remaining_iterations = self.get_iterations()
		cycle = 0

		while remaining_iterations > 0:
			cycle_iterations = remaining_iterations
			if cycle_iterations > self.get_max_concurrency():
				cycle_iterations = self.get_max_concurrency()
			remaining_iterations = remaining_iterations - cycle_iterations

			cycle_initializer, prior_state = create_states_for_cycle(cycle, cycle_iterations, cycle * self.get_max_concurrency(), 
												self.get_branch_state(), self.get_branch_retry_list(),
												self.get_iterator_path(), prior_state, self.get_name())

			if cycle == 0:
				initial_state = cycle_initializer

			cycle = cycle + 1

		finalizer = Pass(Name="{}-Finalizer".format(self.get_name()),
						EndState=True,
						OutputPath="$.[1]")

		consolidator = Task(Name="{}-Consolidator".format(self.get_name()),
						ResourceArn=get_ext_arn(_LIMITED_PARALLEL_CONSOLIDATOR),
						EndState=False,
						NextState=finalizer)

		prior_state.set_end_state(False)
		prior_state.set_next_state(consolidator)

		# Finalizer creates the correct output
		limited_parallel_finalizer = Pass(
			Name="{}-Overall_Finalizer".format(self.get_name()),
			Comment="Creates a list from the list of list of results",
			OutputPath="$.[0]",
			EndState=self.get_end_state(),
			NextState=self.get_next_state())

		# Process in parallel
		limited_parallel_processor = Parallel(
			Name=self.get_name(),
			Comment="Processes the branches limited by MaxConcurrent setting",
			EndState=False,
			NextState=limited_parallel_finalizer,
			InputPath=self.get_input_path(),
			ResultPath=self.get_result_path(),
			OutputPath=self.get_output_path(),
			BranchList=[ initial_state ],
			RetryList=self.get_retry_list(),
			CatcherList=self.get_catcher_list())

		return limited_parallel_processor

	def get_branch_state(self):
		"""
		Returns the initial state for the branch processing

		:returns: ``StateBase`` -- The initial state of the branch
		"""
		return self._branch_state

	def set_branch_state(self, BranchState=None):
		"""
		Set the initial state for the branch processing

		:param BranchState: [Required] ``StateBase`` instance, providing the starting state for each branch to be run concurrently 
		:type: BranchState: ``StateBase``
		"""
		if BranchState and not isinstance(BranchState, StateBase):
			raise Exception("BranchState must either be inherited from StateBase (step '{}')".format(self.get_name()))
		self._branch_state = BranchState

	def get_branch_retry_list(self):
		"""
		Returns the list of ``Retrier`` instances that will be applied separately to each branch execution, allowing failure 
		in one branch iteration during the ``LimitedParallel`` execution to be retried.

		:returns: ``list`` of ``Retrier`` instances
		"""
		return self._lp_branch_retry_list

	def set_branch_retry_list(self, BranchRetryList=None):
		"""
		Sets the list of ``Retrier`` instance to be applied to each of the branch execution in the ``LimitedParallel``.

		If none are specified, then ``LimitedParallel`` will retry at the state level (if ``Retrier`` are specified)

		:param BranchRetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that can be retried for each branch execution
		:type: BranchRetryList: list of ``StateBase``

		"""
		if not BranchRetryList:
			self._lp_branch_retry_list = None
			return

		if not isinstance(BranchRetryList, list):
			raise Exception("BranchRetryList must contain a list of Retrier instances (step '{}')".format(self.get_name()))
		if len(BranchRetryList) == 0:
			raise Exception("BranchRetryList must contain a non-empty list of Retrier instances (step '{}')".format(self.get_name()))
		for o in BranchRetryList:
			if not isinstance(o, Retrier):
				raise Exception("BranchRetryList must contain only instances of Retrier - found '{}' (step '{}')".format(type(o), self.get_name()))
		self._lp_branch_retry_list = [ r for r in BranchRetryList ]

	def get_max_concurrency(self):
		"""
		Returns the maxiumum number of concurrent branch executions

		:returns: ``int`` -- The maximum number of concurrent branch executions
		"""
		return self._max_concurrent

	def set_max_concurrency(self, MaxConcurrency=1):
		"""
		Sets the maximum number of concurrent branch executions, and the supplied value must be greater than zero.  Default is sequential processing.

		:param: MaxConcurrency: [Required] The maximum number of branches that are to executed concurrently.  Must be larger than zero
		:type: MaxConcurrency: int
		"""
		if not MaxConcurrency:
			raise Exception("MaxCurrency must not be None or zero (step '{}')".format(self.get_name()))
		if not isinstance(MaxConcurrency, int):
			raise Exception("MaxCurrency must be an int (step '{}')".format(self.get_name()))
		if MaxConcurrency < 1:
			raise Exception("MaxCurrency must be greater than zero (step '{}')".format(self.get_name()))
		self._max_concurrent = MaxConcurrency

	def get_iterator_path(self):
		"""
		Returns the injection JSONPath to be used to add the iterator value into the Input for a branch

		:returns: str -- The JSONPath for iterator value injection
		"""
		return self._iterator_path

	def set_iterator_path(self, IteratorPath="$.iteration"):
		"""
		Sets the injection JSONPath to use to add the iterator value into the Input for a branch

		:param: IteratorPath: [Required] The JSONPath in which to inject the iterator value into the Input passed to the branch
		:type: IteratorPath: str

		"""
		if not IteratorPath:
			raise Exception("IteratorPath must not be None or empty str (step '{}')".format(self.get_name()))
		if not isinstance(IteratorPath, str):
			raise Exception("IteratorPath must be a str (step '{}')".format(self.get_name()))
		self._iterator_path = IteratorPath

	def get_iterations(self):
		"""
		Returns the total number of branch executions to be performed

		:returns: int -- The total number of branch executions to perform
		"""
		return self._iterations

	def set_iterations(self, Iterations=0):
		"""
		Sets the total number of branch executions to be performed.  Must be larger than zero.

		:param: Iterations: [Required] The total number of branches to be executed.  Must be larger than zero
		:type: Iterations: int
		"""
		if not Iterations:
			raise Exception("Iterations must not be None or zero (step '{}')".format(self.get_name()))
		if not isinstance(Iterations, int):
			raise Exception("Iterations must be an int (step '{}')".format(self.get_name()))
		if Iterations < 1:
			raise Exception("Iterations must be greater than zero (step '{}')".format(self.get_name()))
		self._iterations = Iterations

	def validate(self):
		"""
		Validates this instance is correctly specified.

		Raises ``Exception`` with details of the error, if the state is incorrectly defined.
		
		"""
		# Ensure basic inputs are ok
		super(LimitedParallel, self).validate() 

		# Ensure constructed LimitedParallel is ok
		self._lp_build().validate()

	def to_json(self):
		"""
		Returns the JSON representation of this instance.

		:returns: dict -- The JSON representation
		
		"""
		return self._lp_build().to_json()

	def get_child_states(self):
		# Here we are building a branch "on the fly", so do not call super()
		return self._lp_build().get_child_states()

	def clone(self, NameFormatString="{}"):
		"""
		Returns a clone of this instance, with the clone named per the NameFormatString, to avoid state name clashes.

		If this instance is not an end state, then the next state will also be cloned, to establish a complete clone
		of the branch form this instance onwards.

		:param NameFormatString: [Required] The naming template to be applied to generate the name of the new instance.
		:type NameFormatString: str

		:returns: ``LimitedParallel`` -- A new instance of this instance and any other instances in its branch.
		"""
		if not NameFormatString:
			raise Exception("NameFormatString must not be None (step '{}')".format(self.get_name()))
		if not isinstance(NameFormatString, str):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		c = LimitedParallel(
			Name=NameFormatString.format(self.get_name()),
			Comment=self.get_comment(),
			InputPath=self.get_input_path(),
			OutputPath=self.get_output_path(),
			EndState=self.get_end_state(),
			ResultPath=self.get_result_path(),
			Iterations=self.get_iterations(),
			MaxConcurrent=self.get_max_concurrent(),
			IteratorPath=self.get_iterator_path())

		if self.get_branch_state():
			c.set_branch_state(BranchState=self.get_branch_state().clone(NameFormatString))

		if self.get_branch_retry_list():
			c.set_branch_retry_list(BranchRetryList=self.get_branch_retry_list())

		if self.get_retry_list():
			c.set_retry_list(RetryList=[ r.clone() for r in self.get_retry_list() ])

		if self.get_catcher_list():
			c.set_catcher_list(CatcherList=[ c.clone(NameFormatString) for c in self.get_catcher_list() ])

		if self.get_next_state():
			c.set_next_state(NextState=self.get_next_state.clone(NameFormatString))	

		return c
