from ..pass_state import Pass
from ..task_state import Task
from ..parallel_state import Parallel
from ..state_base import StateBase
from ..retrier import Retrier
from .branch_retry_parallel import BranchRetryParallel

_ext_arns = {}
_INITIALIZER = "ForInitializer"
_EXTRACTOR = "ForExtractor"
_CONSOLIDATOR = "ForConsolidator"
_FINALIZER = "ForFinalizer"
_FINALIZER_PARALLEL_ITERATION = "ForFinalizerParallelIterations"
_LIMITED_PARALLEL_CONSOLIDATOR = "LimitedParallelConsolidator"

def set_ext_arns(ForInitializer=None, ForExtractor=None, ForConsolidator=None,
				ForFinalizer=None, ForFinalizerParallelIterations=None,
				LimitedParallelConsolidator=None):
	"""
	Initialises the ``awssl.ext`` package, so that the correct Lambda functions are used in the ``ext`` states.

	The functions are available in the github repo both as individual lambdas or combined in a CloudFormation script for easy deployment.

	All the Arns must be specified or this function will generate an Exception.

	:param ForInitializer: The Arn of the ForInitializer Lambda function, used by the ``For`` state
	:type ForInitializer: str
	:param ForExtractor: The Arn of the ForExtractor Lambda function, used by the ``For`` state
	:type ForExtractor: str
	:param ForConsolidator: The Arn of the ForConsolidator Lambda function, used by the ``For`` state
	:type ForConsolidator: str
	:param ForFinalizer: The Arn of the ForFinalizer Lambda function, used by the ``For`` state
	:type ForFinalizer: str
	:param ForFinalizerParallelIterations: The Arn of the ForFinalizerParallelIterations Lambda function, used by the ``For`` state
	:type ForFinalizerParallelIterations: str
	:param LimitedParallelConsolidator: The Arn of the LimitedParallelConsolidator Lambda function, used by the ``LimitedParallel`` state
	:type LimitedParallelConsolidator: str

	"""
	def apply_arg(val, val_name):
		if not val:
			raise Exception("set_ext_arns: {} must not be None".format(val_name))
		if not isinstance(val, str):
			raise Exception("set_ext_arns: {} must be a str".format(val_name))
		_ext_arns[val_name] = val

	for v, n in [(ForInitializer, _INITIALIZER), (ForExtractor, _EXTRACTOR),
				(ForConsolidator, _CONSOLIDATOR), (ForFinalizer, _FINALIZER),
				(ForFinalizerParallelIterations, _FINALIZER_PARALLEL_ITERATION),
				(LimitedParallelConsolidator, _LIMITED_PARALLEL_CONSOLIDATOR) ]:
		apply_arg(v, n)

def get_ext_arn(key):
	"""
	Returns the value of the Arn associated with the specified key.

	:param key: The key of the Lambda function whose Arn is required
	:type key: str
	:returns: str
	"""
	arn = _ext_arns.get(key, "")
	if not arn:
		raise Exception("get_ext_arn: Invalid key ({})".format(key))
	return arn

def get_ext_arn_keys():
	"""
	Returns the list of keys against which Arns are defined.

	:returns: list
	"""
	return _ext_arns.keys()

class For(Parallel):
	"""
	Models the ``For`` extension state.

	The ``For`` state constructs and executes branches for each iterator value in the range [``From``, ``To``), incrementing by ``Step``.

	The same branch is repeatedly executed, with the iterator value injected into the Input data at the location specified by ``IteratorPath``.

	The state supports both retry and catch, so that errors can be handled at the state level.  If retries are specified, then all the iterations
	will be re-executed.

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
	:param BranchState: [Required] The starting ``StateBase`` instance of the branch to be executed on each iteration of the ``For`` loop
	:type BranchState: ``StateBase``
	:param BranchRetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that cause the ``For`` loop iteration to be retried.  This will occur until the number of retries has been exhausted for this iteration, afterwhich state level ``Retrier`` will be triggered if specified
	:type BranchRetryList: list of ``Retrier``
	:param From: [Required] The starting value of the iteration.  Must be an integer or float
	:type From: int or float
	:param To: [Required] The ending value of the iteration.  Must be an integer or float
	:type To: int or float
	:param Step: [Required] The incremental value of each iteration.  Must be an integer or float, and cannot be zero.  Default is 1.
	:type To: int or float
	:param IteratorPath: [Required] The JSONPath specifying the injection location for the iterator value into the Input data
	:type IteratorPath: str
	:param ParallelIteration: [Optional] Whether the ``For`` branches can be run concurrently or must be executed sequentially.  Default is sequential.
	:type ParallelIteration: bool

	"""

	def __init__(self, Name=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=False,
					ResultPath="$", RetryList=None, CatcherList=None, BranchState=None, BranchRetryList=None,
					From=0, To=0, Step=1, IteratorPath="$.iteration", ParallelIteration=False):
		"""
		Initializer for the ``For`` class

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
		:param BranchState: [Required] The starting ``StateBase`` instance of the branch to be executed on each iteration of the ``For`` loop
		:type BranchState: ``StateBase``
		:param BranchRetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that cause the ``For`` loop iteration to be retried.  This will occur until the number of retries has been exhausted for this iteration, afterwhich state level ``Retrier`` will be triggered if specified
		:type BranchRetryList: list of ``Retrier``
		:param From: [Required] The starting value of the iteration.  Must be an integer or float
		:type From: int or float
		:param To: [Required] The ending value of the iteration.  Must be an integer or float
		:type To: int or float
		:param Step: [Required] The incremental value of each iteration.  Must be an integer or float, and cannot be zero.  Default is 1.
		:type To: int or float
		:param IteratorPath: [Required] The JSONPath specifying the injection location for the iterator value into the Input data
		:type IteratorPath: str
		:param ParallelIteration: [Optional] Whether the ``For`` branches can be run concurrently or must be executed sequentially.  Default is sequential.
		:type ParallelIteration: bool

		"""
		super(For, self).__init__(Name=Name, Comment=Comment,
			InputPath=InputPath, OutputPath=OutputPath, NextState=NextState, EndState=EndState,
			ResultPath=ResultPath, RetryList=RetryList, CatcherList=CatcherList, BranchList=None)
		self._branch_state = None
		self._from = 0
		self._to = 0
		self._step = 1
		self._iterator_path = None
		self._parallel_iteration = False
		self._f_branch_retry_list = None
		self.set_from(From)
		self.set_to(To)
		self.set_step(Step)
		self.set_iterator_path(IteratorPath)
		self.set_branch_state(BranchState)
		self.set_parallel_iteration(ParallelIteration)
		self.set_branch_retry_list(BranchRetryList)

	def _build_for_loop(self):
		"""
		This does the heavy lifting of declaring the For loop
		"""

		def build_iteration(state_name, cycle, iter_path, iter_value):

			consolidator = Task(
				Name="{}-Consolidator-{}".format(state_name, cycle),
				EndState=False,
				ResourceArn=get_ext_arn(_CONSOLIDATOR))

			injector = Pass(
				Name="{}-PassTask-{}".format(state_name, cycle),
				ResultAsJSON={
					"Iteration": iter_value
				},
				ResultPath=iter_path,
				EndState=False,
				NextState=self.get_branch_state().clone("{}-{}-{}".format(state_name, "{}", cycle)))

			extractor = Task(
				Name="{}-Extractor-{}".format(state_name, cycle),
				EndState=False,
				NextState=injector,
				ResourceArn=get_ext_arn(_EXTRACTOR))

			input_passer = Pass(
				Name="{}-PassInput-{}".format(state_name, cycle),
				EndState=True)

			parallel = BranchRetryParallel(
				Name="{}-ForLoopCycle-{}".format(state_name, cycle),
				BranchList=[input_passer, extractor],
				BranchRetryList=self.get_branch_retry_list(),
				EndState=False,
				NextState=consolidator)

			return { "Parallel" : parallel, "Consolidator" : consolidator }

		finalizer = Pass(
			Name="{}-Finalizer".format(self.get_name()),
			ResultAsJSON=[],
			EndState=True)

		branch_start_state = finalizer

		iter_values = range(self.get_from(), self.get_to(), self.get_step())

		if len(iter_values) > 0:
			finalizer = Task(
				Name="{}-Finalizer".format(self.get_name()),
				ResourceArn=get_ext_arn(_FINALIZER),
				EndState=True)

			initializer = Task(
					Name="{}-Initializer".format(self.get_name()),
					ResourceArn=get_ext_arn(_INITIALIZER),
					EndState=False)

			cycles = []
			for iter_value in iter_values:
				cycles.append(build_iteration(self.get_name(), len(cycles), self.get_iterator_path(), iter_value))

			if not self.get_parallel_iteration():
				# Looping will be sequential

				for i in range(1, len(cycles)):
					cycles[i-1]["Consolidator"].set_next_state(cycles[i]["Parallel"])

				cycles[len(cycles)-1]["Consolidator"].set_next_state(finalizer)

				initializer.set_next_state(cycles[0]["Parallel"])

			else:
				# Looping will be concurrent - assumes all looping is independent

				branch_list = []
				for cycle in cycles:
					branch_list.append(cycle["Parallel"])
					cycle["Consolidator"].set_end_state(True)

				parallel = Parallel(
					Name="{}-Looper".format(self.get_name()),
					EndState=False,
					NextState=finalizer,
					BranchList=branch_list)

				initializer.set_next_state(parallel)
				finalizer.set_resource_arn(ResourceArn=get_ext_arn(_FINALIZER_PARALLEL_ITERATION))

			branch_start_state = initializer

		super(For, self).set_branch_list(BranchList=[branch_start_state])
		super(For, self).set_output_path(OutputPath="$.[0]")

	def get_from(self):
		"""
		Returns the starting value for the ``For`` loop

		:returns: int or float
		"""
		return self._from

	def set_from(self, From=0):
		"""
		Sets the starting value for the ``For`` loop.  Must be an integer or float.  Default value is zero.

		:param From: [Required] The starting value of the iteration.
		:type From: int or float
		"""
		if not isinstance(From, (int, float)):
			raise Exception("From must be either an int or a float (step '{}')".format(self.get_name()))
		self._from = From

	def get_to(self):
		"""
		Returns the ending value for the ``For`` loop

		:returns: int or float
		"""
		return self._to

	def set_to(self, To=0):
		"""
		Sets the ending value for the ``For`` loop.  Must be an integer or float.  Default value is zero.

		:param To: [Required] The ending value of the iteration.
		:type To: int or float
		"""
		if not isinstance(To, (int, float)):
			raise Exception("To must be either an int or a float (step '{}')".format(self.get_name()))
		self._to = To

	def get_step(self):
		"""
		Returns the increment value for the ``For`` loop

		:returns: int or float
		"""
		return self._step

	def set_step(self, Step=1):
		"""
		Sets the increment value for the ``For`` loop.  Must be an integer or float.  Default value is 1.

		:param Step: [Required] The increment value of the iteration.
		:type Step: int or float
		"""
		if not isinstance(Step, (int, float)):
			raise Exception("Step must be either an int or a float (step '{}')".format(self.get_name()))
		if Step == 0:
			raise Exception("Step must not be 0 (step '{}')".format(self.get_name()))
		self._step = Step

	def get_branch_state(self):
		"""
		Returns the starting state of the branch to be executed within the ``For`` loop.

		:returns: ``StateBase``
		"""
		return self._branch_state

	def set_branch_state(self, BranchState=None):
		"""
		Sets the starting state of the branch to be executed within the ``For`` loop.

		:param BranchState: [Required] The starting ``StateBase`` instance of the branch to be executed on each iteration of the ``For`` loop
		:type BranchState: ``StateBase``

		"""
		if BranchState and not isinstance(BranchState, StateBase):
			raise Exception("BranchState must either be inherited from StateBase (step '{}')".format(self.get_name()))
		self._branch_state = BranchState

	def get_branch_retry_list(self):
		"""
		Returns the list of ``Retrier`` instances that will be applied separately to each ``For`` branch iteration, allowing failure
		in one branch iteration during the ``For`` loop to be retried without having to re-execute all the branches of the ``For``.

		:returns: ``list`` of ``Retrier`` instances
		"""
		return self._f_branch_retry_list

	def set_branch_retry_list(self, BranchRetryList=None):
		"""
		Sets the list of ``Retrier`` instance to be applied to each of the branch iterations in the ``For``.

		If none are specified, then ``For`` will retry at the state level (if ``Retrier`` are specified)

		:param BranchRetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that can be retried for each branch iteration
		:type: BranchRetryList: list of ``StateBase``

		"""
		if not BranchRetryList:
			self._f_branch_retry_list = None
			return

		if not isinstance(BranchRetryList, list):
			raise Exception("BranchRetryList must contain a list of Retrier instances (step '{}')".format(self.get_name()))
		if len(BranchRetryList) == 0:
			raise Exception("BranchRetryList must contain a non-empty list of Retrier instances (step '{}')".format(self.get_name()))
		for o in BranchRetryList:
			if not isinstance(o, Retrier):
				raise Exception("BranchRetryList must contain only instances of Retrier - found '{}' (step '{}')".format(type(o), self.get_name()))
		self._f_branch_retry_list = [ r for r in BranchRetryList ]

	def get_iterator_path(self):
		"""
		Returns the JSON Path of the injection location, into which the loop iterator value will be added, as the Input data is passed to the branch.

		:returns: str
		"""
		return self._iterator_path

	def set_iterator_path(self, IteratorPath="$.iteration"):
		"""
		Sets the JSON Path of the injection location, into which the loop iterator value will be added, as the Input data is passed to the branch.

		:param IteratorPath: [Required] The JSONPath specifying the injection location for the iterator value into the Input data
		:type IteratorPath: str
		"""
		self._iterator_path = IteratorPath

	def get_parallel_iteration(self):
		"""
		Returns whether the ``For`` loop will execute concurrently or sequentially.

		:returns: bool
		"""
		return self._parallel_iteration

	def set_parallel_iteration(self, ParallelIteration=False):
		"""
		Specifies whether the execution of the ``For`` loop can be performed concurrently, or must be sequential.  Default is sequential.

		:param ParallelIteration: [Optional] Whether the ``For`` branches can be run concurrently or must be executed sequentially.
		:type ParallelIteration: bool
		"""
		self._parallel_iteration = ParallelIteration

	def validate(self):
		"""
		Validates this instance is correctly specified.

		Raises ``Exception`` with details of the error, if the state is incorrectly defined.

		"""
		self._build_for_loop()
		super(For, self).validate()

	def to_json(self):
		"""
		Returns the JSON representation of this instance.

		:returns: dict -- The JSON representation

		"""
		self._build_for_loop()
		return super(For, self).to_json()

	def clone(self, NameFormatString="{}"):
		"""
		Returns a clone of this instance, with the clone named per the NameFormatString, to avoid state name clashes.

		If this instance is not an end state, then the next state will also be cloned, to establish a complete clone
		of the branch form this instance onwards.

		:param NameFormatString: [Required] The naming template to be applied to generate the name of the new instance.
		:type NameFormatString: str

		:returns: ``For`` -- A new instance of this instance and any other instances in its branch.
		"""
		if not NameFormatString:
			raise Exception("NameFormatString must not be None (step '{}')".format(self.get_name()))
		if not isinstance(NameFormatString, str):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		c = For(
			Name=NameFormatString.format(self.get_name()),
			Comment=self.get_comment(),
			InputPath=self.get_input_path(),
			OutputPath=self.get_output_path(),
			EndState=self.get_end_state(),
			ResultPath=self.get_result_path(),
			From=self.get_from(),
			To=self.get_to(),
			Step=self.get_step(),
			IteratorPath=self.get_iterator_path(),
			ParallelIteration=self.get_parallel_iteration())

		if self.get_branch_state():
			c.set_branch_state(BranchState=self.get_branch_state().clone(NameFormatString))

		if self.get_retry_list():
			c.set_retry_list(RetryList=[ r.clone() for r in self.get_retry_list() ])

		if self.get_catcher_list():
			c.set_catcher_list(CatcherList=[ c.clone(NameFormatString) for c in self.get_catcher_list() ])

		if self.get_next_state():
			c.set_next_state(NextState=self.get_next_state.clone(NameFormatString))

		return c
