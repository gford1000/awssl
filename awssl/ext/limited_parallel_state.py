from ..pass_state import Pass 
from ..task_state import Task 
from ..parallel_state import Parallel
from ..state_base import StateBase
from ..state_retry_catch import StateRetryCatch
from .for_state import For, get_ext_arn, _INITIALIZER, _LIMITED_PARALLEL_CONSOLIDATOR

class LimitedParallel(StateRetryCatch):
	"""
	Models a throttled Parallel
	"""

	def __init__(self, Name=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=None, 
					ResultPath="$", RetryList=None, CatcherList=None, BranchState=None, Iterations=0, MaxConcurrency=1, IteratorPath="$.iteration"):
		super(LimitedParallel, self).__init__(Name=Name, Type="Ext", Comment=Comment, 
			InputPath=InputPath, OutputPath=OutputPath, NextState=NextState, EndState=EndState, 
			ResultPath=ResultPath, RetryList=RetryList, CatcherList=CatcherList)
		self._branch_state = None
		self._max_concurrent = 1
		self._iterator_path = None
		self._iterations = 0
		self.set_branch_state(BranchState)
		self.set_max_concurrency(MaxConcurrency)
		self.set_iterator_path(IteratorPath)
		self.set_iterations(Iterations)

	def _build(self):
		"""
		This does the heavy lifting of declaring the LimitedParallel loop
		"""

		def create_states_for_cycle(cycle, iterations, iteration_offset, branch_state, iterator_path, prior_state, state_name):

			for_state = For(Name="{}-For-{}".format(state_name, cycle),
							EndState=True,
							From=iteration_offset, 
							To=iteration_offset+iterations, 
							Step=1, 
							BranchState=branch_state,
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
												self.get_branch_state(), self.get_iterator_path(), prior_state, self.get_name())

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
		return self._branch_state

	def set_branch_state(self, BranchState=None):
		if BranchState and not isinstance(BranchState, StateBase):
			raise Exception("BranchState must either be inherited from StateBase (step '{}')".format(self.get_name()))
		self._branch_state = BranchState

	def get_max_concurrency(self):
		return self._max_concurrent

	def set_max_concurrency(self, MaxConcurrency=1):
		if not MaxConcurrency:
			raise Exception("MaxCurrency must not be None or zero (step '{}')".format(self.get_name()))
		if not isinstance(MaxConcurrency, int):
			raise Exception("MaxCurrency must be an int (step '{}')".format(self.get_name()))
		if MaxConcurrency < 1:
			raise Exception("MaxCurrency must be greater than zero (step '{}')".format(self.get_name()))
		self._max_concurrent = MaxConcurrency

	def get_iterator_path(self):
		return self._iterator_path

	def set_iterator_path(self, IteratorPath="$.iteration"):
		if not IteratorPath:
			raise Exception("IteratorPath must not be None or empty str (step '{}')".format(self.get_name()))
		if not isinstance(IteratorPath, str):
			raise Exception("IteratorPath must be a str (step '{}')".format(self.get_name()))
		self._iterator_path = IteratorPath

	def get_iterations(self):
		return self._iterations

	def set_iterations(self, Iterations=0):
		if not Iterations:
			raise Exception("Iterations must not be None or zero (step '{}')".format(self.get_name()))
		if not isinstance(Iterations, int):
			raise Exception("Iterations must be an int (step '{}')".format(self.get_name()))
		if Iterations < 1:
			raise Exception("Iterations must be greater than zero (step '{}')".format(self.get_name()))
		self._iterations = Iterations

	def validate(self):
		# Ensure basic inputs are ok
		super(LimitedParallel, self).validate() 

		# Ensure constructed LimitedParallel is ok
		processor = self._build()
		processor.validate()

	def to_json(self):
		return self._build().to_json()

	def get_child_states(self):
		# Here we are building a branch "on the fly", so do not call super()
		return self._build().get_child_states()

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

		if self.get_retry_list():
			c.set_retry_list(RetryList=[ r.clone() for r in self.get_retry_list() ])

		if self.get_catcher_list():
			c.set_catcher_list(CatcherList=[ c.clone(NameFormatString) for c in self.get_catcher_list() ])

		if self.get_next_state():
			c.set_next_state(NextState=self.get_next_state.clone(NameFormatString))	

		return c
