from ..state_retry_catch import StateRetryCatch
from ..parallel_state import Parallel
from ..pass_state import Pass
from ..state_base import StateBase
from ..catcher import Catcher

class StateRetryCatchFinally(StateRetryCatch):
	"""
	Extends StateRetryCatch to add a ``finally`` capability, whose branch will be executed prior to the state completion, or
	the next state after a catch.

		TaskWithFinally, ParallelWithFinally
	"""

	def __init__(self, Name=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=None, ResultPath="$", RetryList=None, CatcherList=None, FinallyState=None):
		super(StateRetryCatchFinally, self).__init__(Name=Name, Type="Ext", Comment=Comment, 
			InputPath=InputPath, OutputPath=OutputPath, NextState=NextState, EndState=EndState, 
			ResultPath=ResultPath, RetryList=RetryList, CatcherList=CatcherList)
		self._finally_branch = None
		self._constructed_states = None
		self.set_finally_branch(FinallyState)

	def _changed(self):
		self._constructed_states = None

	def _get_underlying_state_no_retry_catch(self, state_name):
		# Should be implemented by concrete states
		raise Exception("Concrete state not fully implemented (step '{}')".format(self.get_name()))

	def _srcf_build(self):

		if self._constructed_states:
			return self._constructed_states

		# Retrieve underlying state
		s = self._get_underlying_state_no_retry_catch(self.get_name())
		if not s or not isinstance(s, (StateRetryCatch)):
			raise Exception("Returned concrete state must be derived from StateRetryCatch (step '()')".format(self.get_name()))

		s.set_comment(Comment=self.get_comment())
		s.set_input_path(InputPath=self.get_input_path())
		s.set_output_path(OutputPath=self.get_output_path())
		s.set_result_path(ResultPath=self.get_result_path())
		s.set_retry_list(RetryList=self.get_retry_list())

		if self.get_finally_branch():
			# Ensure no results passed on from the Finally branch
			no_result_pass = Pass(
				Name="{}-FinallyTerminator".format(self.get_name()),
				Comment="Finally branch should never return any results",
				ResultAsJSON={},
				EndState=True,
				NextState=None)

			# Catch any errors issued by executing the finally branch
			catcher = Catcher(
				ErrorNameList=[ "States.All"],
				NextState=no_result_pass)

			# Execute the finally branch in a Parallel, as it could be multi-step
			finally_parallel = Parallel(
				Name="{}-Finally".format(self.get_name()),
				Comment="Parallel to allow error catching on arbitrary finally processing",
				BranchList=[self._finally_branch],
				CatcherList=[catcher],
				EndState=False,
				NextState=no_result_pass)

			# Results pass through state
			pass_through_pass = Pass(
				Name="{}-PassThrough".format(self.get_name()),
				Comment="Ensures that the original result is preserved",
				EndState=True,
				NextState=None)

			# Final state for successful execution - extracts the results from the embedded state
			extractor_pass = Pass(
				Name="{}-Extractor".format(self.get_name()),
				Comment="Ensures the original result from the state is returned",
				OutputPath="$.[0]",
				EndState=self.get_end_state(),
				NextState=self.get_next_state())

			# Post parallel executes the finally, also passing through the result from the prior state
			post_parallel = Parallel(
				Name="{}-PostParallel".format(self.get_name()),
				BranchList=[pass_through_pass, finally_parallel],
				EndState=True,
				NextState=False)

			# Clone for each catcher
			new_catcher_list = None
			if self.get_catcher_list():
				new_catcher_list = []
				offset = 0
				for catcher in self.get_catcher_list():
					catcher_extractor = Pass(
						Name="{}-Extractor-Catcher-{}".format(self.get_name(), offset),
						Comment="Ensures the original result from the state is passed to the supplied catcher, after the finally branch has completed",
						OutputPath="$.[0]",
						EndState=False,
						NextState=catcher.get_next_state())
					catcher_parallel = post_parallel.clone("{}-Catcher-{}".format("{}", offset))
					catcher_parallel.set_comment(Comment="Parallel to manage finally, before supplied catcher is executed")
					catcher_parallel.set_end_state(False)
					catcher_parallel.set_next_state(catcher_extractor)
					new_catcher_list.append(Catcher(ErrorNameList=catcher.get_error_name_list(), NextState=catcher_parallel))
					offset = offset + 1

			# Now apply the normal next state
			post_parallel.set_comment(Comment="Parallel to manage finally, for successful completion of state")
			post_parallel.set_end_state(EndState=False)
			post_parallel.set_next_state(NextState=extractor_pass)

			# Ensure the finally branch is executed
			s.set_catcher_list(CatcherList=new_catcher_list)
			s.set_end_state(EndState=False)
			s.set_next_state(NextState=post_parallel)

		else:
			# No finally branch supplied
			s.set_catcher_list(CatcherList=self.get_catcher_list())
			s.set_end_state(EndState=self.get_end_state())
			s.set_next_state(NextState=self.get_next_state())

		self._constructed_states = s
		return self._constructed_states

	def get_child_states(self):
		# Builds a stand alone branch, so return that rather than self
		self.validate()
		return self._srcf_build().get_child_states()

	def validate(self):
		self._srcf_build().validate()

	def to_json(self):
		return self._srcf_build().to_json()

	def get_finally_branch(self):
		return self._finally_branch

	def set_finally_branch(self, FinallyState=None):
		if FinallyState:
			if not isinstance(FinallyState, StateBase):
				raise Exception("FinallyState must inherited from StateBase, for step ({})".format(self.get_name()))
		self._finally_branch = FinallyState

