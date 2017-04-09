from .state_base import StateBase

class Catcher(object):
	"""
	Models a Catcher for a "Catch" field in a Task or Parallel state
	"""

	def __init__(self, ErrorNameList=None, NextState=None):
		self._error_name_list = None
		self._next_state = None
		self.set_error_name_list(ErrorNameList)
		self.set_next_state(NextState)

	def get_error_name_list(self):
		return self._error_name_list

	def set_error_name_list(self, ErrorNameList):
		if not ErrorNameList:
			raise Exception("ErrorNameList must not be None for a Catcher")
		if not isinstance(ErrorNameList, list):
			raise Exception("ErrorNameList must be a list for a Catcher")
		if len(ErrorNameList) == 0:
			raise Exception("ErrorNameList must be a non-empty list for a Catcher")
		for o in ErrorNameList:
			if not isinstance(o, str):
				raise Exception("ErrorNameList must only contain strings")
		self._error_name_list = ErrorNameList

	def get_next_state(self):
		return self._next_state

	def set_next_state(self, NextState=None):
		if NextState and not isinstance(NextState, StateBase):
			raise Exception("NextState must be a subclass of StateBase for a Catcher")
		self._next_state = NextState

	def validate(self):
		if not self.get_next_state():
			raise Exception("Catcher must have a NextState")
		if not self.get_error_name_list():
			raise Exception("Catcher must have an ErrorNameList")

	def to_json(self):
		return {
			"ErrorEquals" : self.get_error_name_list(),
			"Next" : self.get_next_state().get_name()
		}

	def clone(self, NameFormatString="{}"):
		"""
		Returns a clone of this instance.

		If the next state invoked by this catcher is not an end state, then the next state will also be cloned, to establish a complete clone
		of the branch form this instance onwards.

		:param NameFormatString: [Required] The naming template to be applied to generate the name of next state in the new instance.
		:type NameFormatString: str

		:returns: ``Catcher`` -- A new instance of this instance and any other instances in its branch.
		"""
		if not NameFormatString:
			raise Exception("NameFormatString must not be None (step '{}')".format(self.get_name()))
		if not isinstance(NameFormatString, str):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		c = Catcher()

		if self.get_error_name_list():
			c.set_error_name_list(ErrorNameList=[ n for n in self.get_error_name_list() ])

		if self.get_next_state():
			c.set_next_state(NextState=self.get_next_state.clone(NameFormatString))	

		return c
