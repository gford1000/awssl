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
		self._choice_list = []
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
		if Default and not isinstance(Default, StateBase):
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

	def get_child_states(self):
		states = super(Choice, self).get_child_states()
		for choice in  self.get_choice_list():
			states = states + choice.get_next_state().get_child_states()
		if self.get_default():
			states = states + self.get_default().get_child_states()
		return states

	def clone(self, NameFormatString="{}"):
		"""
		Returns a clone of this instance, with the clone named per the NameFormatString, to avoid state name clashes.

		If this instance is not an end state, then the next state will also be cloned, to establish a complete clone
		of the branch form this instance onwards.

		:param NameFormatString: [Required] The naming template to be applied to generate the name of the new instance.
		:type NameFormatString: str

		:returns: ``Choice`` -- A new instance of this instance and any other instances in its branch.
		"""
		if not NameFormatString:
			raise Exception("NameFormatString must not be None (step '{}')".format(self.get_name()))
		if not isinstance(NameFormatString, str):
			raise Exception("NameFormatString must be a str (step '{}')".format(self.get_name()))

		c = Choice(
			Name=NameFormatString.format(self.get_name()),
			Comment=self.get_comment(),
			InputPath=self.get_input_path(),
			OutputPath=self.get_output_path(),
			ChoiceList=[ c.clone(NameFormatString) for c in self.get_choice_list() ])

		if self.get_default():
			c.set_default(Default=self.get_default().clone(NameFormatString))	

		return c
