from .state_base import StateBase
from .state_next_end import StateNextEnd
import datetime

class Wait(StateNextEnd):

	""" 
	Wait is a Step Function state that pauses execution of the State Machine for a period of time.

	Waits can be durations defined in seconds, or until a specific time.
	Waits can be non-declarative, and instead use values from the Input data to the state.

	Only one method of expressing the Wait can be specified in each Wait state.
	"""

	def __init__(self, Name="", Comment="", InputPath="$", OutputPath="$", EndState=False, NextState=None, 
		WaitForSeconds=None, WaitForSecondsPath=None, WaitUntilISO8601Timestamp=None, WaitUntilISO8601TimestampPath=None):
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
		super(Wait, self).validate()
		if len(self._get_assigned_wait()) != 1:
			raise Exception("Incorrect specification of Wait (step '{}')".format(self.get_name()))

	def to_json(self):
		j = super(Wait, self).to_json()
		for k, v in self._get_assigned_wait().viewitems():
			j[k] = v
		return j

	def get_wait_seconds(self):
		return self._wait_seconds

	def set_wait_seconds(self, WaitForSeconds=1):
		if WaitForSeconds and not isinstance(WaitForSeconds, int):
			raise Exception("WaitForSeconds must be an integer value (step '{}')".format(self.get_name()))
		if WaitForSeconds < 1:
			raise Exception("WaitForSeconds must be a positive integer value (step '{}')".format(self.get_name()))
		self._reset_waits()
		self._wait_seconds = WaitForSeconds

	def get_wait_seconds_path(self):
		return self._wait_seconds_path

	def set_wait_seconds_path(self, WaitForSecondsPath=None):
		if WaitForSecondsPath and not isinstance(WaitForSecondsPath, str):
			raise Exception("WaitForSecondsPath must be an string value (step '{}')".format(self.get_name()))
		self._reset_waits()
		self._wait_seconds_path = WaitForSecondsPath

	def get_wait_timestamp(self):
		return self._wait_timestamp

	def set_wait_timestamp(self, WaitUntilISO8601Timestamp):
		if WaitUntilISO8601Timestamp:
			if not isinstance(WaitUntilISO8601Timestamp, str):
				raise Exception("WaitUntilISO8601Timestamp must be an string value (step '{}')".format(self.get_name()))
			try:
				dt = datetime.datetime.strptime(WaitUntilISO8601Timestamp, "%Y-%m-%dT%H:%M:%SZ")
			except:
				raise Exception("WaitUntilISO8601Timestamp must be UTC datetime, of the form: YYYY-MM-DDTHH:MM:SSZ")
		self._reset_waits()
		self._wait_timestamp = WaitUntilISO8601Timestamp

	def set_wait_timestamp_path(self):
		return self._wait_timestamp_path

	def set_wait_timestamp_path(self, WaitUntilISO8601TimestampPath=None):
		if WaitUntilISO8601TimestampPath and not isinstance(WaitUntilISO8601TimestampPath, str):
			raise Exception("WaitUntilISO8601TimestampPath must be an string value (step '{}')".format(self.get_name()))
		self._reset_waits()
		self._wait_timestamp_path = WaitUntilISO8601TimestampPath


