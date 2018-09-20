from .state_base import StateBase
from .state_input_output import StateInputOutput

class StateNextEnd(StateInputOutput):
	"""
	Base class for States that support Next or End

		Pass, Task, Wait, Parallel
	"""

	def __init__(self, Name=None, Type=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=False):
		super(StateNextEnd, self).__init__(Name, Type, Comment, InputPath, OutputPath)
		self._next_state = None
		self._end_state = False
		self.set_end_state(EndState)
		self.set_next_state(NextState)

	def validate(self):
		super(StateNextEnd, self).validate()
		if (not self._next_state) and not self._end_state:
			raise Exception("Either this step must be specified as an End state, or specify a Next state, for step ({})".format(self.get_name()))
		if self._next_state and self._end_state:
			raise Exception("This step specifies it is an End, but also specifies a Next state, for step ({})".format(self.get_name()))

	def to_json(self):
		j = super(StateNextEnd, self).to_json()
		next_state = self.get_next_state()
		if next_state:
			j["Next"] = next_state.get_name()
		else:
			j["End"] = self.get_end_state()
		return j

	def get_next_state(self):
		return self._next_state

	def set_next_state(self, NextState=None):
		if NextState and not isinstance(NextState, StateBase):
			raise Exception("Invalid NextState specified - must be subclass of StateBase (step: {})".format(self.get_name()))
		self._next_state = NextState
		if self._next_state:
			self._end_state = False
		else:
			self._end_state = True

	def get_end_state(self):
		return self._end_state

	def set_end_state(self, EndState=False):
		if not isinstance(EndState, bool):
			raise Exception("Invalid EndState specified - must be a bool (step: {})".format(self.get_name()))
		self._end_state = EndState
		if self._end_state:
			self._next_state = None

	def get_child_states(self):
		states = super(StateNextEnd, self).get_child_states()
		if not self.get_end_state():
			states.append(self.get_next_state())
		return states
