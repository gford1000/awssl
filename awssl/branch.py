from .state_base import StateBase
from .state_next_end import StateNextEnd
from .state_retry_catch import StateRetryCatch
from .choice_state import Choice


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
			raise Exception("StateObject must not be None")
		if not isinstance(StateObject, StateBase):
			raise Exception("StateObject must be inherited from StateBase")
		self._start_state = StateObject

	def _build_states(self):
		def add(current_state, states):
			if not current_state:
				return
			if not current_state in states:
				states.append(current_state)
			if isinstance(current_state, Choice):
				for choice in current_state.get_choice_list():
					add(choice.get_next_state(), states)
				add(current_state.get_default(), states)
			if isinstance(current_state, StateRetryCatch):
				if current_state.get_catcher_list() and len(current_state.get_catcher_list()) > 0:
					for catcher in current_state.get_catcher_list():
						add(catcher.get_next_state(), states)
			if isinstance(current_state, StateNextEnd):
				next_state = current_state.get_next_state()
				if isinstance(next_state, (list, tuple)):
					for s in next_state:
						add(s, states)
				else:
					add(next_state, states)

		states = []
		if self._start_state:
			add(self._start_state, states)
		return states

	def to_json(self):
		j = {
			"StartAt" : self._start_state.get_name(),
			"States" : {}
		}
		for s in self._build_states():
			j["States"][s.get_name()] = s.to_json()
		return j

	def validate(self):
		for s in self._build_states():
			s.validate()
