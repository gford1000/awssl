from .state_base import StateBase

class Catcher(object):
	"""
	Models a ``Catcher`` that can be used in a ``Task`` or ``Parallel`` state to catch errors and then redirect the ``StateMachine``
	to another state to continue processing.

	:param ErrorNameList: [Required] The set of error names that this ``Catcher`` will handle.
	:type ErrorNameList: list of str
	:param NextState: [Required] Next state to be invoked within this branch.
	:type NextState: instance of class derived from ``StateBase``

	"""

	def __init__(self, ErrorNameList=None, NextState=None):
		"""
		Initializer for the Catcher.

		:param ErrorNameList: [Required] The set of error names that this ``Catcher`` will handle.
		:type ErrorNameList: list of str
		:param NextState: [Required] Next state to be invoked within this branch.
		:type NextState: instance of class derived from ``StateBase``

		"""
		self._error_name_list = None
		self._next_state = None
		self.set_error_name_list(ErrorNameList)
		self.set_next_state(NextState)

	def get_error_name_list(self):
		"""
		Returns the ``list`` of error names that this instance will handle.

		:returns: list of str -- The list of error names
		"""
		return self._error_name_list

	def set_error_name_list(self, ErrorNameList):
		"""
		Sets the ``list`` of error names that this instance will handle.

		``ErrorNameList`` must not be ``None``, and must be a non-empty ``list`` of ``str``.

		:param ErrorNameList: [Required] The set of error names that this ``Catcher`` will handle.
		:type ErrorNameList: list of str

		"""
		if not ErrorNameList:
			raise Exception("ErrorNameList must not be None for a Catcher")
		if not isinstance(ErrorNameList, list):
			raise Exception("ErrorNameList must be a list for a Catcher")
		if len(ErrorNameList) == 0:
			raise Exception("ErrorNameList must be a non-empty list for a Catcher")
		for o in ErrorNameList:
			if not isinstance(o, basestring):
				raise Exception("ErrorNameList must only contain strings")
		self._error_name_list = ErrorNameList

	def get_next_state(self):
		"""
		Returns the ``StateBase`` instance that will be invoked if this ``Catcher`` traps an error

		:returns: ``StateBase`` -- The next state to be invoked
		"""
		return self._next_state

	def set_next_state(self, NextState=None):
		"""
		Sets the next state to be invoked if any of the specified error conditions occur.  ``NextState`` must not be ``None``.

		:param NextState: [Required] Next state to be invoked within this branch.
		:type NextState: instance of class derived from ``StateBase``

		"""
		if NextState and not isinstance(NextState, StateBase):
			raise Exception("NextState must be a subclass of StateBase for a Catcher")
		self._next_state = NextState

	def validate(self):
		"""
		Validates this instance is correctly specified.

		Raises ``Exception`` with details of the error, if the instance is incorrectly defined.

		"""
		if not self.get_next_state():
			raise Exception("Catcher must have a NextState")
		if not self.get_error_name_list():
			raise Exception("Catcher must have an ErrorNameList")

	def to_json(self):
		"""
		Returns the JSON representation of this instance.

		:returns: dict -- The JSON representation

		"""
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
		if not isinstance(NameFormatString, basestring):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		cloned_error_name_list = None
		if self.get_error_name_list():
			cloned_error_name_list = [ n for n in self.get_error_name_list() ]

		cloned_next_state = None
		if self.get_next_state():
			cloned_next_state = self.get_next_state().clone(NameFormatString)

		return Catcher(ErrorNameList=cloned_error_name_list, NextState=cloned_next_state)
