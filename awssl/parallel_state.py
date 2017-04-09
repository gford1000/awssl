from .state_base import StateBase
from .state_retry_catch import StateRetryCatch
from .branch import Branch

class Parallel(StateRetryCatch):
	"""
	Models a Parallel state
	"""

	def __init__(self, Name=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=None, 
					ResultPath="$", RetryList=None, CatcherList=None, BranchList=None):
		super(Parallel, self).__init__(Name=Name, Type="Parallel", Comment=Comment, 
			InputPath=InputPath, OutputPath=OutputPath, NextState=NextState, EndState=EndState, 
			ResultPath=ResultPath, RetryList=RetryList, CatcherList=CatcherList)
		self._branches = None
		self.set_branch_list(BranchList)

	def add_branch(self, StartObject=None):
		if not StartObject:
			raise Exception("StartObject must not be None for a Branch (step '{}'".format(self.get_name()))
		if not isinstance(StartObject, StateBase):
			raise Exception("BranchList must contain only subclasses of StateBase (step '{}'".format(self.get_name()))
		if not self._branches:
			self._branches = []
		self._branches.append(Branch(StartObject))

	def set_branch_list(self, BranchList=None):
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

	def validate(self):
		super(Parallel, self).validate()

		if (not self._branches) or len(self._branches) == 0: 
			raise Exception("Parallel state must contain at least one branch (step '{}'".format(self.get_name()))
		for b in self._branches:
			b.validate()

	def to_json(self):
		if (not self._branches) or len(self._branches) == 0: 
			raise Exception("Parallel state must contain at least one branch (step '{}'".format(self.get_name()))

		branches = []
		for b in self._branches:
			branches.append(b.to_json())

		j = super(Parallel, self).to_json()
		j["Branches"] = branches
		return j

	def clone(self, NameFormatString="{}"):
		"""
		Returns a clone of this instance, with the clone named per the NameFormatString, to avoid state name clashes.

		If this instance is not an end state, then the next state will also be cloned, to establish a complete clone
		of the branch form this instance onwards.

		:param NameFormatString: [Required] The naming template to be applied to generate the name of the new instance.
		:type NameFormatString: str

		:returns: ``Parallel`` -- A new instance of this instance and any other instances in its branch.
		"""
		if not NameFormatString:
			raise Exception("NameFormatString must not be None (step '{}')".format(self.get_name()))
		if not isinstance(NameFormatString, str):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		c = Parallel(
			Name=NameFormatString.format(self.get_name()),
			Comment=self.get_comment(),
			InputPath=self.get_input_path(),
			OutputPath=self.get_output_path(),
			EndState=self.get_end_state(),
			ResultPath=self.get_result_path())

		if self.get_retry_list():
			c.set_retry_list(RetryList=[ r.clone() for r in self.get_retry_list() ])

		if self.get_catcher_list():
			c.set_catcher_list(CatcherList=[ c.clone(NameFormatString) for c in self.get_catcher_list() ])

		if self._branches:
			c.set_branch_list(BranchList=[ b.get_start_state().clone(NameFormatString) for b in self._branches ])

		if self.get_next_state():
			c.set_next_state(NextState=self.get_next_state().clone(NameFormatString))	

		return c
