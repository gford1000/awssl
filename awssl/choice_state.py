from .state_base import StateBase
from .state_input_output import StateInputOutput
from .choice_rule import ChoiceRule
from .not_choice_rule import NotChoiceRule
from .and_choice_rule import AndChoiceRule
from .or_choice_rule import OrChoiceRule

class Choice(StateInputOutput):
	"""
	Models the Choice state, which allows multiple Choice Rules to be tested, and to redirect to the 
	state specified by the first Choice Rule that passes.

	If no Choice Rules pass, then the State Machine redirects to the state specified as Default (if one)

	"""
	def __init__(self, Name="", Comment="", InputPath="$", OutputPath="$", ChoiceList=[], Default=None):
		super(Choice, self).__init__(Name=Name, Type="Choice", Comment=Comment, InputPath=InputPath, OutputPath=OutputPath)
		self._choce_list = []
		self._default = None
		self.set_choice_list(ChoiceList)
		self.set_default(Default)

	def get_choice_list(self):
		return self._choice_list

	def set_choice_list(self, ChoiceList=[]):
		if not ChoiceList:
			raise Exception("ChoiceList must not be None for a Choice (step '{}')".format(self.get_name()))
		if not isinstance(ChoiceList, list):
			raise Exception("ChoiceList must be a list for a Choice (step '{}')".format(self.get_name()))
		if len(ChoiceList) == 0:
			raise Exception("ChoiceList must be a non-empty list for a Choice (step '{}')".format(self.get_name()))
		for o in ChoiceList:
			if not isinstance(o, (ChoiceRule, NotChoiceRule, AndChoiceRule, OrChoiceRule)):
				raise Exception("ChoiceList items must be of types (ChoiceRule, NotChoiceRule, AndChoiceRule, OrChoiceRule) for a Choice (step '{}')".format(self.get_name()))
		self._choice_list = ChoiceList

	def get_default(self):
		return self._default

	def set_default(self, Default=None):
		if (not Default) and not isinstance(Default, StateBase):
			raise Exception("Default for a Choice must reference an instance of StateBase (step '{}')".format(self.get_name()))
		self._default = Default

	def validate(self):
		super(Choice, self).validate()
		for o in self.get_choice_list():
			o.validate()

	def to_json(self):
		choices = []
		for o in self.get_choice_list():
			choices.append(o.to_json())

		j = super(Choice, self).to_json()
		j["Choices"] = choices 
		if self.get_default():
			j["Default"] = self.get_default().get_name()
		return j

