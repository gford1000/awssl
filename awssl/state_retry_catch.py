from .state_result import StateResult
from .retrier import Retrier
from .catcher import Catcher

class StateRetryCatch(StateResult):
	"""
	Base class for States that support Retries and Catches

		Task, Parallel
	"""

	def __init__(self, Name=None, Type=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=None, ResultPath="$", RetryList=None, CatcherList=None):
		super(StateRetryCatch, self).__init__(Name=Name, Type=Type, Comment=Comment, 
			InputPath=InputPath, OutputPath=OutputPath, NextState=NextState, EndState=EndState, ResultPath=ResultPath)
		self._retry_list = None
		self._catcher_list = None
		self.set_retry_list(RetryList)
		self.set_catcher_list(CatcherList)

	def validate(self):
		super(StateRetryCatch, self).validate()
		if self.get_retry_list():
			for o in self.get_retry_list():
				o.validate()
		if self.get_catcher_list():
			for o in self.get_catcher_list():
				o.validate()

	def to_json(self):
		j = super(StateRetryCatch, self).to_json()
		if self.get_retry_list():
			retriers = []
			for o in self.get_retry_list():
				retriers.append(o.to_json())
			j["Retry"] = retriers
		if self.get_catcher_list():
			catchers = []
			for o in self.get_catcher_list():
				catchers.append(o.to_json())
			j["Catch"] = catchers
		return j

	def get_retry_list(self):
		return self._retry_list

	def set_retry_list(self, RetryList=None):
		if RetryList:
			if not isinstance(RetryList, list):
				raise Exception("RetryList must be a list, for step ({})".format(self.get_name()))
			if len(RetryList) == 0:
				raise Exception("RetryList must be a non-empty list, or None, for step ({})".format(self.get_name()))
			for o in RetryList:
				if not isinstance(o, Retrier):
					raise Exception("RetryList must be a list of Retrier objects, for step ({})".format(self.get_name()))
		self._retry_list = RetryList

	def get_catcher_list(self):
		return self._catcher_list

	def set_catcher_list(self, CatcherList=None):
		if CatcherList:
			if not isinstance(CatcherList, list):
				raise Exception("CatcherList must be a list, for step ({})".format(self.get_name()))
			if len(CatcherList) == 0:
				raise Exception("CatcherList must be a non-empty list, or None, for step ({})".format(self.get_name()))
			for o in CatcherList:
				if not isinstance(o, Catcher):
					raise Exception("CatcherList must be a list of Catcher objects, for step ({})".format(self.get_name()))
		self._catcher_list = CatcherList
