from .state_base import StateBase

class Branch(object):
	"""
	Branch of processing within a StateMachine or Parallel Task.
	"""

	def __init__(self, StateObject=None):
		self._start_state = None
		self.set_start_state(StateObject)

	def get_start_state(self):
		return self._start_state

	def set_start_state(self, StateObject=None):
		if not StateObject:
			self._start_state = StateObject
			return

		if not isinstance(StateObject, StateBase):
			raise Exception("StateObject must be inherited from StateBase")
		self._start_state = StateObject

	def _build_states(self):
		def add(new_states, state_list):
			for state in new_states:
				if state and state not in state_list:
					state_list.append(state)
					add(state.get_child_states(), state_list)

		states = []
		if self.get_start_state():
			add(self.get_start_state().get_child_states(), states)
		return states

	def to_json(self):
		j = {
			"StartAt" : self.get_start_state().get_name(),
			"States" : {}
		}
		for s in self._build_states():
			j["States"][s.get_name()] = s.to_json()
		return j

	def validate(self):
		if not self._start_state:
			raise Exception("StartState of Branch must not be None")
		for s in self._build_states():
			s.validate()
