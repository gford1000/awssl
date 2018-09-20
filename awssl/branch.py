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
		states = []
		states.append(self.get_start_state())
		reached_states = []
		while len(states)>0 :
			current_state = states.pop()
			reached_states.append(current_state)
			childrens = current_state.get_child_states()
			for child in childrens :
				if child and child not in reached_states:
					states.append(child)
		return reached_states

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
