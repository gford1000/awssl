from .state_retry_catch import StateRetryCatch

class Task(StateRetryCatch):
	"""
	Models a Task state
	"""

	def __init__(self, Name=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=None, 
					ResultPath="$", RetryList=None, CatcherList=None,
					ResourceArn=None, TimeoutSeconds=60, HeartbeatSeconds=None):
		super(Task, self).__init__(Name=Name, Type="Task", Comment=Comment, 
			InputPath=InputPath, OutputPath=OutputPath, NextState=NextState, EndState=EndState, 
			ResultPath=ResultPath, RetryList=RetryList, CatcherList=CatcherList)
		self._resource_arn = None
		self._timeout_seconds = None
		self._heartbeat_seconds = None
		self.set_resource_arn(ResourceArn)

	def validate(self):
		super(Task, self).validate()

	def to_json(self):
		j = super(Task, self).to_json()
		j["Resource"] = self.get_resource_arn()
		if self.get_timeout_seconds():
			j["TimeoutSeconds"] = self.get_timeout_seconds()
		if self.get_heartbeat_seconds():
			j["HeartbeatSeconds"] = self.get_heartbeat_seconds()
		return j

	def get_resource_arn(self):
		return self._resource_arn

	def set_resource_arn(self, ResourceArn=None):
		if not ResourceArn:
			raise Exception("ResourceArn must be specified for Task state (step '{}')".format(self.get_name()))
		if not isinstance(ResourceArn, str):
			raise Exception("ResourceArn must be a string for Task state (step '{}')".format(self.get_name()))
		self._resource_arn = ResourceArn

	def get_timeout_seconds(self):
		return self._timeout_seconds

	def set_timeout_seconds(self, TimeoutSeconds=60):
		if TimeoutSeconds:
			if not isinstance(TimeoutSeconds, int):
				raise Exception("TimeoutSeconds must be an integer if specified for Task (step '{}')".format(self.get_name()))
			if TimeoutSeconds < 1:
				raise Exception("TimeoutSeconds must be greater than zero if specified for Task (step '{}')".format(self.get_name()))
		self._timeout_seconds = TimeoutSeconds

	def get_heartbeat_seconds(self):
		return self._heartbeat_seconds

	def set_heartbeat_seconds(self, HeartbeatSeconds=None):
		if HeartbeatSeconds:
			if not isinstance(HeartbeatSeconds, int):
				raise Exception("HeartbeatSeconds must be an integer if specified for Task (step '{}')".format(self.get_name()))
			if HeartbeatSeconds < 1:
				raise Exception("HeartbeatSeconds must be greater than zero if specified for Task (step '{}')".format(self.get_name()))
		self._heartbeat_seconds = HeartbeatSeconds

