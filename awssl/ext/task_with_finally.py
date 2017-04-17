from .state_retry_catch_finally import StateRetryCatchFinally
from ..task_state import Task

class TaskWithFinally(StateRetryCatchFinally):
	"""
	The ``TaskWithFinally`` state can be used to invoke either an AWS Lambda function or an ``Activity``, which provides a general mechanism for all
	types of processing.  The Task supports retries and catching of specified errors to provide structured error handling, as well
	as supporting Timeout for processing as one of those error types.

	As its name suggests, ``TaskWithFinally`` also allows a branch to be executed after a successful completion of the task,
	or if any of the ``Catcher`` s are triggered by an error.  

	Note that the finally branch will not be executed if no ``Catcher`` traps the error, so it is recommended that a ``Catcher`` is
	provided that traps ``States.ALL`` if the finally branch must always be executed.

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
	:param ResultPath: [Optional] JSONPath indicating where results should be added to the Input.  Defaults to "$", indicating results replace the Input entirely.
	:type ResultPath: str
	:param RetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that cause the entire set of branches to be retried
	:type: RetryList: list of ``Retrier``
	:param CatcherList: [Optional] ``list`` of ``Catcher`` instances corresponding to error states that can be caught and handled by further states being executed in the ``StateMachine``.
	:type: CatcherList: list of ``Catcher``
	:param FinallyState: [Required] First state of the finally branch to be invoked
	:type: FinallyState: Derived from ``StateBase``
	:param ResourceArn: [Required] The Arn for the ``Lambda`` function or ``Activity`` that the ``Task`` should invoke
	:type: ResourceArn: str
	:param: TimeoutSeconds: [Optional] The number of seconds in which the ``Task`` should complete
	:type: TimeoutSeconds: int
	:param: HeartbeatSeconds: [Optional]  The number of seconds between heartbeats from an ``Activity``, to indicate it is still running
	:type: HeartbeatSeconds: int

	"""

	def __init__(self, Name=None, Comment="", InputPath="$", OutputPath="$", NextState=None, EndState=None, 
					ResultPath="$", RetryList=None, CatcherList=None, FinallyState=None,
					ResourceArn=None, TimeoutSeconds=99999999, HeartbeatSeconds=99999999):
		"""
		Initializer for the TaskWithFinally state

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
		:param ResultPath: [Optional] JSONPath indicating where results should be added to the Input.  Defaults to "$", indicating results replace the Input entirely.
		:type ResultPath: str
		:param RetryList: [Optional] ``list`` of ``Retrier`` instances corresponding to error states that cause the entire set of branches to be retried
		:type: RetryList: list of ``Retrier``
		:param CatcherList: [Optional] ``list`` of ``Catcher`` instances corresponding to error states that can be caught and handled by further states being executed in the ``StateMachine``.
		:type: CatcherList: list of ``Catcher``
		:param FinallyState: [Required] First state of the finally branch to be invoked
		:type: FinallyState: Derived from ``StateBase``
		:param ResourceArn: [Required] The Arn for the ``Lambda`` function or ``Activity`` that the ``Task`` should invoke
		:type: ResourceArn: str
		:param: TimeoutSeconds: [Optional] The number of seconds in which the ``Task`` should complete
		:type: TimeoutSeconds: int
		:param: HeartbeatSeconds: [Optional]  The number of seconds between heartbeats from an ``Activity``, to indicate it is still running
		:type: HeartbeatSeconds: int

		"""
		super(TaskWithFinally, self).__init__(Name=Name, Comment=Comment, 
			InputPath=InputPath, OutputPath=OutputPath, NextState=NextState, EndState=EndState, 
			ResultPath=ResultPath, RetryList=RetryList, CatcherList=CatcherList, FinallyState=FinallyState)
		self._resource_arn = None
		self._timeout_seconds = None
		self._heartbeat_seconds = None
		self.set_resource_arn(ResourceArn)
		self.set_timeout_seconds(TimeoutSeconds)
		self.set_heartbeat_seconds(HeartbeatSeconds)

	def _get_underlying_state_no_retry_catch(self, state_name):
		return Task(
			Name=state_name,
			ResourceArn=self.get_resource_arn(),
			TimeoutSeconds=self.get_timeout_seconds(),
			HeartbeatSeconds=self.get_heartbeat_seconds(),
			EndState=True)

	def get_resource_arn(self):
		"""
		Returns the Arn of the Lambda or ``Activity`` that will be invoked by this ``TaskWithFinally``.

		:returns: str -- The Arn of the resource to be invoked.
		"""
		return self._resource_arn

	def set_resource_arn(self, ResourceArn=None):
		"""
		Sets the Arn of the Lambda of ``Activity`` to be invoked by this ``TaskWithFinally``.  Cannot be ``None`` and must be a valid Arn formatted string.

		:param ResourceArn: [Required] The Arn for the ``Lambda`` function or ``Activity`` that the ``TaskWithFinally`` should invoke
		:type: ResourceArn: str		
		"""
		if not ResourceArn:
			raise Exception("ResourceArn must be specified for TaskWithFinally state (step '{}')".format(self.get_name()))
		if not isinstance(ResourceArn, str):
			raise Exception("ResourceArn must be a string for TaskWithFinally state (step '{}')".format(self.get_name()))
		self._resource_arn = ResourceArn

	def get_timeout_seconds(self):
		"""
		Returns the timeout seconds for the ``TaskWithFinally``, afterwhich a ``States.Timeout`` error is raised.

		:returns: int -- The timeout seconds for the state.
		"""
		return self._timeout_seconds

	def set_timeout_seconds(self, TimeoutSeconds=99999999):
		"""
		Sets the timeout seconds for the ``TaskWithFinally``, afterwhich a ``States.Timeout`` error is raised.

		If specified, must not be less than zero seconds.  Default value is ``99999999``.

		:param: TimeoutSeconds: [Optional] The number of seconds in which the ``TaskWithFinally`` should complete
		:type: TimeoutSeconds: int
		"""
		if TimeoutSeconds:
			if not isinstance(TimeoutSeconds, int):
				raise Exception("TimeoutSeconds must be an integer if specified for TaskWithFinally (step '{}')".format(self.get_name()))
			if TimeoutSeconds < 1:
				raise Exception("TimeoutSeconds must be greater than zero if specified for TaskWithFinally (step '{}')".format(self.get_name()))
		self._timeout_seconds = TimeoutSeconds

	def get_heartbeat_seconds(self):
		"""
		Returns the heartbeat interval for the ``TaskWithFinally``.  If more than two heartbeats are missed then the state will
		fail with a ``States.Timeout`` error.

		:returns: int -- The heartbeat seconds for the state.
		"""
		return self._heartbeat_seconds

	def set_heartbeat_seconds(self, HeartbeatSeconds=99999999):
		"""
		Sets the heartbeats seconds for the ``TaskWithFinally``.  If more than two heartbeats are missed then the state will
		fail with a ``States.Timeout`` error.

		If specified, must not be less than zero seconds.  Default value is ``99999999``.

		:param: HeartbeatSeconds: [Optional]  The number of seconds between heartbeats from an ``Activity``, to indicate it is still running
		:type: HeartbeatSeconds: int
		"""
		if HeartbeatSeconds:
			if not isinstance(HeartbeatSeconds, int):
				raise Exception("HeartbeatSeconds must be an integer if specified for TaskWithFinally (step '{}')".format(self.get_name()))
			if HeartbeatSeconds < 1:
				raise Exception("HeartbeatSeconds must be greater than zero if specified for TaskWithFinally (step '{}')".format(self.get_name()))
		self._heartbeat_seconds = HeartbeatSeconds

	def clone(self, NameFormatString="{}"):
		"""
		Returns a clone of this instance, with the clone named per the NameFormatString, to avoid state name clashes.

		If this instance is not an end state, then the next state will also be cloned, to establish a complete clone
		of the branch form this instance onwards.

		:param NameFormatString: [Required] The naming template to be applied to generate the name of the new instance.
		:type NameFormatString: str

		:returns: ``TaskWithFinally`` -- A new instance of this instance and any other instances in its branch.
		"""
		if not NameFormatString:
			raise Exception("NameFormatString must not be None (step '{}')".format(self.get_name()))
		if not isinstance(NameFormatString, str):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		c = TaskWithFinally(
			Name=NameFormatString.format(self.get_name()),
			Comment=self.get_comment(),
			InputPath=self.get_input_path(),
			OutputPath=self.get_output_path(),
			EndState=self.get_end_state(),
			ResultPath=self.get_result_path(),
			ResourceArn=self.get_resource_arn(),
			TimeoutSeconds=self.get_timeout_seconds(),
			HeartbeatSeconds=self.get_heartbeat_seconds())

		if self.get_retry_list():
			c.set_retry_list(RetryList=[ r.clone() for r in self.get_retry_list() ])

		if self.get_catcher_list():
			c.set_catcher_list(CatcherList=[ c.clone(NameFormatString) for c in self.get_catcher_list() ])

		if self.get_next_state():
			c.set_next_state(NextState=self.get_next_state.clone(NameFormatString))	

		if self.get_finally_state():
			c.set_finally_state(FinallyState=self.get_finally_state().clone(NameFormatString))

		return c
