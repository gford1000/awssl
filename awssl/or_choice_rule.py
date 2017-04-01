from .comparison import Comparison
from .state_base import StateBase

class OrChoiceRule(object):
	"""
	Tests a list of Comparisons in the order of the comparison list provided

	Returns True if any Comparisons return True, otherwise False
	"""

	def __init__(self, ComparisonList=[], NextState=None):
		self._comparison_list = None
		self._next_state = None
		self.set_comparison_list(ComparisonList)
		self.set_next_state(NextState)

	def get_comparison_list(self):
		return self._comparison_list

	def set_comparison_list(self, ComparisonList=[]):
		if not ComparisonList:
			raise Exception("ComparisonList must not be None for a OR ChoiceRule")
		if not isinstance(ComparisonList, list):
			raise Exception("ComparisonList must be a List of Comparison objects")
		if len(ComparisonList) == 0:
			raise Exception("ComparisonList must be a non-empty List of Comparison objects")
		for o in ComparisonList:
			if not isinstance(o, Comparison):
				raise Exception("ComparisonList must only contain Comparison objects")
		self._comparison_list = ComparisonList

	def get_next_state(self):
		return self._next_state

	def set_next_state(self, NextState=None):
		if NextState and not isinstance(NextState, StateBase):
			raise Exception("Invalid NextState for ChoiceRule, which must be subclass of StateBase")
		self._next_state = NextState

	def validate(self):
		if not self.get_next_state():
			raise Exception("Invalid ChoiceRule - must declare NextState")
		for comparison in self.get_comparison_list():
			comparison.validate()

	def to_json(self):
		l = []
		for comparison in self.get_comparison_list():
			l.append(comparison.to_json())
		return {
			"Or" : l,
			"Next" : self.get_next_state().get_name()
		}
