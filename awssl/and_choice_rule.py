from .comparison import Comparison
from .state_base import StateBase

class AndChoiceRule(object):
	"""
	Tests a list of Comparisons in the order of the comparison list provided

	Returns True if all Comparisons return True, otherwise False
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
			raise Exception("ComparisonList must not be None for an AND ChoiceRule")
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
			"And" : l,
			"Next" : self.get_next_state().get_name()
		}

	def clone(self, NameFormatString="{}"):
		"""
		Returns a clone of this instance.

		The NameFormatString will be used to clone the next state that this Choice Rule will initiate if triggered.

		:param NameFormatString: [Required] The naming template to be applied to generate the name of the next state.
		:type NameFormatString: str

		:returns: ``AndChoiceRule`` -- A new instance of this instance and any other instances in its branch.
		"""
		if not NameFormatString:
			raise Exception("NameFormatString must not be None (step '{}')".format(self.get_name()))
		if not isinstance(NameFormatString, basestring):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		c = AndChoiceRule()

		if self.get_comparison_list():
			c.set_comparison_list(ComparisonList=[ c.clone() for c in self.get_comparison_list() ])

		if self.get_next_state():
			c.set_next_state(NextState=self.get_next_state().clone(NameFormatString))

		return c
