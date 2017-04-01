from .comparison import Comparison
from .state_base import StateBase

class NotChoiceRule(object):
	"""
	Returns the opposite of the result of the Comparison
	"""

	def __init__(self, Comparison=None, NextState=None):
		self._comparison = None
		self._next_state = None
		self.set_comparison(Comparison)
		self.set_next_state(NextState)

	def get_comparison(self):
		return self._comparison

	def set_comparison(self, Comparison=None):
		if not Comparison:
			raise Exception("Comparison must not be null in a ChoiceRule")
		if not isinstance(Comparison, Comparison):
			raise Exception("Invalid object - must be of type Comparison")
		self._comparison = Comparison

	def get_next_state(self):
		return self._next_state

	def set_next_state(self, NextState=None):
		if NextState and not isinstance(NextState, StateBase):
			raise Exception("Invalid NextState for ChoiceRule, which must be subclass of StateBase")
		self._next_state = NextState

	def validate(self):
		if not self.get_comparison():
			raise Exception("Invalid ChoiceRule - must declare Comparison")
		if not self.get_next_state():
			raise Exception("Invalid ChoiceRule - must declare NextState")
		self.get_comparison().validate()

	def to_json(self):
		return {
			"Not" : self.get_comparison().to_json(),
			"Next" : self.get_next_state().get_name()
		}


