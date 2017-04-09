from .comparison import Comparison as ComparisonObject
from .state_base import StateBase

class ChoiceRule(object):
	"""
	Returns the result of the Comparison
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
		if not isinstance(Comparison, ComparisonObject):
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
		j = self.get_comparison().to_json()
		j["Next"] = self.get_next_state().get_name()
		return j

	def clone(self, NameFormatString="{}"):
		"""
		Returns a clone of this instance.

		The NameFormatString will be used to clone the next state that this Choice Rule will initiate if triggered.

		:param NameFormatString: [Required] The naming template to be applied to generate the name of the next state.
		:type NameFormatString: str

		:returns: ``ChoiceRule`` -- A new instance of this instance and any other instances in its branch.
		"""
		if not NameFormatString:
			raise Exception("NameFormatString must not be None (step '{}')".format(self.get_name()))
		if not isinstance(NameFormatString, str):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		c = ChoiceRule()

		if self.get_comparison():
			c.set_comparison(Comparison=self.get_comparison().clone())	

		if self.get_next_state():
			c.set_next_state(NextState=self.get_next_state().clone(NameFormatString))

		return c
