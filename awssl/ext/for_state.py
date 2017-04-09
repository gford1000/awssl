from ..pass_state import Pass 
from ..task_state import Task 
from ..parallel_state import Parallel
from ..state_base import StateBase

_for_arns = {}
_INITIALIZER = "Initializer"
_EXTRACTOR = "Extractor"
_CONSOLIDATOR = "Consolidator"
_FINALIZER = "Finalizer"

def set_for_arns(Initializer=None, Extractor=None, Consolidator=None, Finalizer=None):
	def apply_arg(val, val_name):
		if not val:
			raise Exception("set_for_arn: {} must not be None".format(val_name))
		if not isinstance(val, str):
			raise Exception("set_for_arn: {} must be a str".format(val_name))
		_for_arns[val_name] = val

	for v, n in [(Initializer, _INITIALIZER), (Extractor, _EXTRACTOR), (Consolidator, _CONSOLIDATOR), (Finalizer, _FINALIZER)]:
		apply_arg(v, n)

def get_for_arn(key):
	arn = _for_arns.get(key, "")
	if not arn:
		raise Exception("get_for_arn: Invalid key ({})".format(key))
	return arn

class For(Parallel):
	"""
	Models a declared for loop, iterating between From until To, advancing by Step
	"""

	def __init__(self, Name=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=None, 
					ResultPath="$", RetryList=None, CatcherList=None, BranchState=None, From=0, To=0, Step=1, IteratorPath="$.iteration"):
		super(For, self).__init__(Name=Name, Comment=Comment, 
			InputPath=InputPath, OutputPath=OutputPath, NextState=NextState, EndState=EndState, 
			ResultPath=ResultPath, RetryList=RetryList, CatcherList=CatcherList, BranchList=None)
		self._branch_state = None
		self._from = 0 
		self._to = 0
		self._step = 1
		self._iterator_path = None
		self.set_from(From)
		self.set_to(To)
		self.set_step(Step)
		self.set_iterator_path(IteratorPath)
		self.set_branch_state(BranchState)

	def _build_for_loop(self):
		"""
		This does the heavy lifting of declaring the For loop
		"""

		def build_iteration(state_name, cycle, iter_path, iter_value):

			consolidator = Task(
				Name="{}-Consolidator-{}".format(state_name, cycle),
				EndState=False,
				ResourceArn=get_for_arn(_CONSOLIDATOR))

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
				ResourceArn=get_for_arn(_EXTRACTOR))

			input_passer = Pass(
				Name="{}-PassInput-{}".format(state_name, cycle),
				EndState=True)

			parallel = Parallel(
				Name="{}-ForLoopCycle-{}".format(state_name, cycle),
				BranchList=[input_passer, extractor],
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
				EndState=True,
				ResourceArn=get_for_arn(_FINALIZER))

			cycles = []
			for iter_value in iter_values:
				cycles.append(build_iteration(self.get_name(), len(cycles), self.get_iterator_path(), iter_value))

			for i in range(1, len(cycles)):
				cycles[i-1]["Consolidator"].set_next_state(cycles[i]["Parallel"])

			cycles[len(cycles)-1]["Consolidator"].set_next_state(finalizer)

			initializer = Task(
					Name="{}-Initializer".format(self.get_name()),
					ResourceArn=get_for_arn(_INITIALIZER),
					EndState=False,
					NextState=cycles[0]["Parallel"])

			branch_start_state = initializer

		super(For, self).set_branch_list(BranchList=[branch_start_state])
		super(For, self).set_output_path(OutputPath="$.[0]")

	def get_from(self):
		return self._from

	def set_from(self, From=0):
		if not isinstance(From, (int, float)):
			raise Exception("From must be either an int or a float (step '{}')".format(self.get_name()))
		self._from = From

	def get_to(self):
		return self._to

	def set_to(self, To=0):
		if not isinstance(To, (int, float)):
			raise Exception("To must be either an int or a float (step '{}')".format(self.get_name()))
		self._to = To

	def get_step(self):
		return self._step

	def set_step(self, Step=1):
		if not isinstance(Step, (int, float)):
			raise Exception("Step must be either an int or a float (step '{}')".format(self.get_name()))
		if Step == 0:
			raise Exception("Step must not be 0 (step '{}')".format(self.get_name()))
		self._step = Step

	def get_branch_state(self):
		return self._branch_state

	def set_branch_state(self, BranchState=None):
		if BranchState and not isinstance(BranchState, StateBase):
			raise Exception("BranchState must either be inherited from StateBase (step '{}')".format(self.get_name()))
		self._branch_state = BranchState

	def get_iterator_path(self):
		return self._iterator_path

	def set_iterator_path(self, IteratorPath="$.iteration"):
		self._iterator_path = IteratorPath

	def validate(self):
		self._build_for_loop()
		super(For, self).validate()

	def to_json(self):
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
