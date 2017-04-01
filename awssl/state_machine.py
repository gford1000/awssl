from .branch import Branch
from json import dumps

class StateMachine(object):

	def __init__(self, Comment="", ASLVersion="1.0", StartState=None):
		self._comment = ""
		self._asl_version = ""
		self._branch = None
		self.set_comment(Comment)
		self.set_asl_version(ASLVersion)
		self.set_start_state(StartState)

	def get_start_state(self):
		return self._branch.get_start_state()

	def set_start_state(self, StartState=None):
		self._branch = Branch(StartState)

	def get_comment(self):
		return self._comment

	def set_comment(self, Comment=""):
		if not Comment:
			Comment = ""
		self._comment = Comment

	def get_asl_version(self):
		return self._asl_version

	def set_asl_version(self, ASLVersion="1.0"):
		if not ASLVersion:
			ASLVersion = "1.0"
		if ASLVersion != "1.0":
			raise Exception("Only version 1.0 of ASL is supported")
		self._asl_version = ASLVersion

	def __str__(self):
		self.validate()

		j = self._branch.to_json()
		j["Comment"] = self.get_comment()
		j["Version"] = self.get_asl_version()

		return dumps(j, sort_keys=True, indent=4)

	def validate(self):
		if not self._branch:
			raise Exception("StartState must be specified for the StateMachine")

		self._branch.validate()
