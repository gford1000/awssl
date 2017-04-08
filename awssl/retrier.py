class Retrier(object):
	"""
	Models a Retrier for a "Retry" field in a Task or Parallel state

	:param ErrorNameList: [Required] The set of error names that this ``Retrier`` will handle.
	:type ErrorNameList: list of str
	:param IntervalSeconds: [Optional] The interval in seconds before retrying the state.  Default is 1 second.
	:type IntervalSeconds: int
	:param MaxAttempts: [Optional] The maximum number of retry attempts.  Default is 3.
	:type MaxAttempts: int
	:param BackoffRate: [Optional] The growth rate in retry interval.  Must be greater than 1.0.  Default is 2.0.
	:type BackoffRate: float

	"""

	def __init__(self, ErrorNameList=None, IntervalSeconds=1, MaxAttempts=3, BackoffRate=2.0):
		"""
		Initializer for this instance

		:param ErrorNameList: [Required] The set of error names that this ``Retrier`` will handle.
		:type ErrorNameList: list of str
		:param IntervalSeconds: [Optional] The interval in seconds before retrying the state.  Default is 1 second.
		:type IntervalSeconds: int
		:param MaxAttempts: [Optional] The maximum number of retry attempts.  Default is 3.
		:type MaxAttempts: int
		:param BackoffRate: [Optional] The growth rate in retry interval.  Must be greater than 1.0.  Default is 2.0.
		:type BackoffRate: float

		"""
		self._error_name_list = None
		self._interval_seconds = 1
		self._max_attempts = 3
		self._back_off_rate = 2.0
		self.set_error_name_list(ErrorNameList)
		self.set_interval_seconds(IntervalSeconds)
		self.set_max_attempts(MaxAttempts)
		self.set_backoff_rate(BackoffRate)

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

		:param ErrorNameList: [Required] The set of error names that this ``Retrier`` will handle.
		:type ErrorNameList: list of str

		"""
		if not ErrorNameList:
			raise Exception("ErrorNameList must not be None for a Retrier")
		if not isinstance(ErrorNameList, list):
			raise Exception("ErrorNameList must be a list for a Retrier")
		if len(ErrorNameList) == 0:
			raise Exception("ErrorNameList must be a non-empty list for a Retrier")
		for o in ErrorNameList:
			if not isinstance(o, str):
				raise Exception("ErrorNameList must only contain strings")
		self._error_name_list = ErrorNameList

	def get_interval_seconds(self):
		"""
		Returns the interval in seconds before the state machine will retry the associated failed state.

		:returns: int -- The interval in seconds before retrying.

		"""
		return self._interval_seconds

	def set_interval_seconds(self, IntervalSeconds=1):
		"""
		Sets the interval in seconds before the state machine will retry the associated failed state.

		The interval must be >= 1 second.  Default is 1 second.

		:param IntervalSeconds: [Optional] The interval in seconds before retrying the state.  
		:type IntervalSeconds: int		

		"""
		if not IntervalSeconds:
			raise Exception("IntervalSeconds must not be None for a Retrier")
		if not isinstance(IntervalSeconds, int):
			raise Exception("IntervalSeconds must be an integer value")
		if IntervalSeconds < 1:
			raise Exception("IntervalSeconds must be greater than 1 second")
		self._interval_seconds = IntervalSeconds

	def get_max_attempts(self):
		"""
		Returns the maximum number of retry attempts of the associated failed state.

		:returns: int -- The maximum number of retry attempts.
		"""
		return self._max_attempts

	def set_max_attempts(self, MaxAttempts=3):
		"""
		Sets the maximum number of retry attempts of the associated failed state.

		The max attempts must be greater than or equal to zero.  A value of zero indicates that no retry will be attempted.  The default is 3.

		:param MaxAttempts: [Optional] The maximum number of retry attempts.
		:type MaxAttempts: int

		"""
		if not MaxAttempts:
			raise Exception("MaxAttempts must not be None for a Retrier")
		if not isinstance(MaxAttempts, int):
			raise Exception("MaxAttempts must be an integer value")
		if MaxAttempts < 0:
			raise Exception("MaxAttempts must be 0 or greater")
		self._max_attempts = MaxAttempts

	def get_backoff_rate(self):
		"""
		Returns the backoff rate that will be applied to the ``IntervalSeconds`` on each retry.

		:returns: float -- The backoff rate for the ``IntervalSeconds``.
		"""
		return self._back_off_rate

	def set_backoff_rate(self, BackoffRate=2.0):
		"""
		Sets the backoff rate that will be applied to the ``IntervalSeconds`` after the first retry.

		The backoff rate must be >= 1.0.  Default is 2.0.

		:param BackoffRate: [Optional] The growth rate in retry interval.
		:type BackoffRate: float

		"""
		if not BackoffRate:
			raise Exception("BackoffRate must not be None for a Retrier")
		if not isinstance(BackoffRate, float):
			raise Exception("BackoffRate must be an float value")
		if BackoffRate < 1.0:
			raise Exception("BackoffRate must be greater or equal to 1.0")
		self._back_off_rate = BackoffRate

	def validate(self):
		"""
		Validates this instance is correctly specified.

		Raises ``Exception`` with details of the error, if the state machine is incorrectly defined.
		
		"""
		if not self.get_error_name_list():
			raise Exception("Retrier must have an ErrorNameList")

	def to_json(self):
		"""
		Returns the JSON representation of this instance.

		:returns: dict -- The JSON representation
		
		"""
		return {
			"ErrorEquals" : self.get_error_name_list(),
			"IntervalSeconds" : self.get_interval_seconds(),
			"MaxAttempts" : self.get_max_attempts(),
			"BackoffRate" : self.get_backoff_rate()
		}
