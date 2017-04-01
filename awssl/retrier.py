class Retrier(object):
	"""
	Models a Retrier for a "Retry" field in a Task or Parallel state
	"""

	def __init__(self, ErrorNameList=None, IntervalSeconds=1, MaxAttempts=3, BackoffRate=2.0):
		self._error_name_list = None
		self._interval_seconds = 1
		self._max_attempts = 3
		self._back_off_rate = 2.0
		self.set_error_name_list(ErrorNameList)
		self.set_interval_seconds(IntervalSeconds)
		self.set_max_attempts(MaxAttempts)
		self.set_backoff_rate(BackoffRate)

	def get_error_name_list(self):
		return self._error_name_list

	def set_error_name_list(self, ErrorNameList):
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
		return self._interval_seconds

	def set_interval_seconds(self, IntervalSeconds=1):
		if not IntervalSeconds:
			raise Exception("IntervalSeconds must not be None for a Retrier")
		if not isinstance(IntervalSeconds, int):
			raise Exception("IntervalSeconds must be an integer value")
		if IntervalSeconds < 1:
			raise Exception("IntervalSeconds must be greater than 1 second")
		self._interval_seconds = IntervalSeconds

	def get_max_attempts(self):
		return self._max_attempts

	def set_max_attempts(self, MaxAttempts=3):
		if not MaxAttempts:
			raise Exception("MaxAttempts must not be None for a Retrier")
		if not isinstance(MaxAttempts, int):
			raise Exception("MaxAttempts must be an integer value")
		if MaxAttempts < 0:
			raise Exception("MaxAttempts must be 0 or greater")
		self._max_attempts = MaxAttempts

	def get_backoff_rate(self):
		return self._back_off_rate

	def set_backoff_rate(self, BackoffRate=2.0):
		if not BackoffRate:
			raise Exception("BackoffRate must not be None for a Retrier")
		if not isinstance(BackoffRate, float):
			raise Exception("BackoffRate must be an float value")
		if BackoffRate < 1.0:
			raise Exception("BackoffRate must be greater or equal to 1.0")
		self._back_off_rate = BackoffRate

	def validate(self):
		if not self.get_error_name_list():
			raise Exception("Retrier must have an ErrorNameList")

	def to_json(self):
		return {
			"ErrorEquals" : self.get_error_name_list(),
			"IntervalSeconds" : self.get_interval_seconds(),
			"MaxAttempts" : self.get_max_attempts(),
			"BackoffRate" : self.get_backoff_rate()
		}
