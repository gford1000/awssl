from .state_base import StateBase
from .state_next_end import StateNextEnd
import datetime

class Wait(StateNextEnd):
	"""
	Wait is a Step Function state that pauses execution of the State Machine for a period of time.

	Waits can be durations defined in seconds, or until a specific time.
	Waits can be non-declarative, and instead use values from the Input data to the state.

	One (and only one) method of expressing the wait can be specified in each Wait state.

	Either:

	* ``EndState`` is ``True`` and ``NextState`` must be ``None``
	* ``EndState`` is ``False`` and ``NextState`` must be a valid instance of a class derived from ``StateBase``.

	:param Name: [Required] The name of the state within the branch of the state machine
	:type Name: str
	:param Comment: [Optional] A comment describing the intent of this pass state
	:type Comment: str
	:param InputPath: [Optional] Filter on the Input information to be passed to the Pass state.  Default is "$", signifying that all the Input information will be provided
	:type InputPath: str
	:param OutputPath: [Optional] Filter on the Output information to be returned from the Pass state.  Default is "$", signifying that all the result information will be provided
	:type OutputPath: str
	:param EndState: [Optional] Flag indicating if this state terminates a branch of the state machine.  Defaults to ``False``
	:type EndState: bool
	:param NextState: [Optional] Next state to be invoked within this branch.  Must not be ``None`` unless ``EndState`` is ``True``
	:type NextState: instance of class derived from ``StateBase``
	:param WaitForSeconds: [Optional] The number of seconds of the wait interval.  If specified, this must be a positive integer.
	:type WaitForSeconds: int
	:param WaitForSecondsPath: [Optional] A JSONPath to a wait interval within the Input data provided to the state.
	:type WaitForSecondsPath: str
	:param WaitUntilISO8601Timestamp: [Optional] A datetime string that conforms to the RFC3339 profile of ISO 8601.
	:type WaitUntilISO8601Timestamp: str
	:param WaitUntilISO8601TimestampPath: [Optional] A JSONPath to a datetime string that conforms to the RFC3339 profile of ISO 8601, within the Input data provided to the state.
	:type WaitUntilISO8601TimestampPath: str

	"""

	def __init__(self, Name="", Comment="", InputPath="$", OutputPath="$", EndState=False, NextState=None,
		WaitForSeconds=None, WaitForSecondsPath=None, WaitUntilISO8601Timestamp=None, WaitUntilISO8601TimestampPath=None):
		"""
		Initialize for the Wait class

		:param Name: [Required] The name of the state within the branch of the state machine
		:type Name: str
		:param Comment: [Optional] A comment describing the intent of this pass state
		:type Comment: str
		:param InputPath: [Optional] Filter on the Input information to be passed to the Pass state.  Default is "$", signifying that all the Input information will be provided
		:type InputPath: str
		:param OutputPath: [Optional] Filter on the Output information to be returned from the Pass state.  Default is "$", signifying that all the result information will be provided
		:type OutputPath: str
		:param EndState: [Optional] Flag indicating if this state terminates a branch of the state machine.  Defaults to ``False``
		:type EndState: bool
		:param NextState: [Optional] Next state to be invoked within this branch.  Must not be ``None`` unless ``EndState`` is ``True``
		:type NextState: instance of class derived from ``StateBase``
		:param WaitForSeconds: [Optional] The number of seconds of the wait interval.  If specified, this must be a positive integer.
		:type WaitForSeconds: int
		:param WaitForSecondsPath: [Optional] A JSONPath to a wait interval within the Input data provided to the state.
		:type WaitForSecondsPath: str
		:param WaitUntilISO8601Timestamp: [Optional] A datetime string that conforms to the RFC3339 profile of ISO 8601.
		:type WaitUntilISO8601Timestamp: str
		:param WaitUntilISO8601TimestampPath: [Optional] A JSONPath to a datetime string that conforms to the RFC3339 profile of ISO 8601, within the Input data provided to the state.
		:type WaitUntilISO8601Timestamp: str

		"""
		super(Wait, self).__init__(Name=Name, Type="Wait", Comment=Comment, InputPath=InputPath, OutputPath=OutputPath, EndState=EndState, NextState=NextState)
		self._reset_waits()
		if WaitForSeconds:
			self.set_wait_seconds(WaitForSeconds)
		if WaitForSecondsPath:
			self.set_wait_seconds_path(WaitForSecondsPath)
		if WaitUntilISO8601Timestamp:
			self.set_wait_timestamp(WaitUntilISO8601Timestamp)
		if WaitUntilISO8601TimestampPath:
			self.set_wait_timestamp_path(WaitUntilISO8601TimestampPath)

	def _get_assigned_wait(self):
		assigned = {}
		if self._wait_seconds:
			assigned = { "Seconds": self._wait_seconds }
		if self._wait_seconds_path:
			assigned = { "SecondsPath": self._wait_seconds_path }
		if self._wait_timestamp:
			assigned = { "Timestamp": self._wait_timestamp }
		if self._wait_timestamp_path:
			assigned = { "TimestampPath": self._wait_timestamp_path }
		return assigned

	def _reset_waits(self):
		self._wait_seconds = None
		self._wait_seconds_path = None
		self._wait_timestamp = None
		self._wait_timestamp_path = None

	def validate(self):
		"""
		Validates this instance is correctly specified.

		Raises ``Exception`` with details of the error, if the state is incorrectly defined.

		"""
		super(Wait, self).validate()
		if len(self._get_assigned_wait()) != 1:
			raise Exception("Incorrect specification of Wait (step '{}')".format(self.get_name()))

	def to_json(self):
		"""
		Returns the JSON representation of this instance.

		:returns: dict -- The JSON representation

		"""
		j = super(Wait, self).to_json()
		for k, v in self._get_assigned_wait().viewitems():
			j[k] = v
		return j

	def get_wait_seconds(self):
		"""
		Returns the wait interval in seconds.

		:returns: int -- The wait interval
		"""
		return self._wait_seconds

	def set_wait_seconds(self, WaitForSeconds=1):
		"""
		Sets the wait interval in seconds.

		The interval must be a positive integer if specifed.  Default value is 1 second.

		:param WaitForSeconds: [Optional] The number of seconds of the wait interval.  If specified, this must be a positive integer.
		:type WaitForSeconds: int

		"""
		if WaitForSeconds and not isinstance(WaitForSeconds, int):
			raise Exception("WaitForSeconds must be an integer value (step '{}')".format(self.get_name()))
		if WaitForSeconds < 1:
			raise Exception("WaitForSeconds must be a positive integer value (step '{}')".format(self.get_name()))
		self._reset_waits()
		self._wait_seconds = WaitForSeconds

	def get_wait_seconds_path(self):
		"""
		Returns the JSON Path with which to resolve the wait interval from the Input data supplied to the state.

		:returns: str
		"""
		return self._wait_seconds_path

	def set_wait_seconds_path(self, WaitForSecondsPath=None):
		"""
		Sets the JSON Path with which to resolve the wait interval from the Input data supplied to the state.

		:param WaitForSecondsPath: [Optional] A JSONPath to a wait interval within the Input data provided to the state.
		:type WaitForSecondsPath: str

		"""
		if WaitForSecondsPath and not isinstance(WaitForSecondsPath, basestring):
			raise Exception("WaitForSecondsPath must be an string value (step '{}')".format(self.get_name()))
		self._reset_waits()
		self._wait_seconds_path = WaitForSecondsPath

	def get_wait_timestamp(self):
		"""
		Returns a timestamp as the RFC3339 profile of ISO 8601.  The wait will stop its branch of the ``StateMachine`` until this time has passed

		:returns: str
		"""
		return self._wait_timestamp

	def set_wait_timestamp(self, WaitUntilISO8601Timestamp):
		"""
		Sets a date/time of the format RFC3339 profile of ISO 8601.  The wait will stop its branch of the ``StateMachine`` until this time has passed

		:param WaitUntilISO8601Timestamp: [Optional] A datetime string that conforms to the RFC3339 profile of ISO 8601.
		:type WaitUntilISO8601Timestamp: str
		"""
		if WaitUntilISO8601Timestamp:
			if not isinstance(WaitUntilISO8601Timestamp, basestring):
				raise Exception("WaitUntilISO8601Timestamp must be an string value (step '{}')".format(self.get_name()))
			try:
				dt = datetime.datetime.strptime(WaitUntilISO8601Timestamp, "%Y-%m-%dT%H:%M:%SZ")
			except:
				raise Exception("WaitUntilISO8601Timestamp must be UTC datetime, of the form: YYYY-MM-DDTHH:MM:SSZ")
		self._reset_waits()
		self._wait_timestamp = WaitUntilISO8601Timestamp

	def get_wait_timestamp_path(self):
		"""
		Returns the JSON Path with which to resolve the wait date/time from the Input data supplied to the state.

		:returns: str
		"""
		return self._wait_timestamp_path

	def set_wait_timestamp_path(self, WaitUntilISO8601TimestampPath=None):
		"""
		Sets a JSON Path of a date/time of the format RFC3339 profile of ISO 8601, which will be retrieved from the Input data passed to the state.

		The wait will stop its branch of the ``StateMachine`` until this time has passed

		:param WaitUntilISO8601TimestampPath: [Optional] A JSONPath to a datetime string that conforms to the RFC3339 profile of ISO 8601, within the Input data provided to the state.
		:type WaitUntilISO8601Timestamp: str
		"""
		if WaitUntilISO8601TimestampPath and not isinstance(WaitUntilISO8601TimestampPath, basestring):
			raise Exception("WaitUntilISO8601TimestampPath must be an string value (step '{}')".format(self.get_name()))
		self._reset_waits()
		self._wait_timestamp_path = WaitUntilISO8601TimestampPath

	def clone(self, NameFormatString="{}"):
		"""
		Returns a clone of this instance, with the clone named per the NameFormatString, to avoid state name clashes.

		If this instance is not an end state, then the next state will also be cloned, to establish a complete clone
		of the branch form this instance onwards.

		:param NameFormatString: [Required] The naming template to be applied to generate the name of the new instance.
		:type NameFormatString: str

		:returns: ``Wait`` -- A new instance of this instance and any other instances in its branch.
		"""
		if not NameFormatString:
			raise Exception("NameFormatString must not be None (step '{}')".format(self.get_name()))
		if not isinstance(NameFormatString, basestring):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		c = Wait(
			Name=NameFormatString.format(self.get_name()),
			Comment=self.get_comment(),
			InputPath=self.get_input_path(),
			OutputPath=self.get_output_path(),
			EndState=self.get_end_state(),
			WaitForSeconds=self.get_wait_seconds(),
			WaitForSecondsPath=self.get_wait_seconds_path(),
			WaitUntilISO8601Timestamp=self.get_wait_timestamp(),
			WaitUntilISO8601TimestampPath=self.get_wait_timestamp_path())

		if self.get_next_state():
			c.set_next_state(NextState=self.get_next_state().clone(NameFormatString))

		return c
