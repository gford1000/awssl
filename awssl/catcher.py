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
