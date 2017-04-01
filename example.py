import awssl

def example_one():
	# Construct states
	s2 = awssl.Wait(Name="Wait1", EndState=True, WaitForSeconds=2)
	s1 = awssl.Pass(Name="Pass1", NextState=s2)
	s1.set_result({"foo":"bar"})

	# Construct state machine
	sm = awssl.StateMachine(Comment="This is a test")
	sm.set_start_state(s1)
	return sm


def example_two():
	# Choice branches
	fail1= awssl.Fail(Name="Fail1", ErrorName="Outside", ErrorCause="Value < 3 or > 5")
	fail2= awssl.Fail(Name="Fail2", ErrorName="NoSelection", ErrorCause="Unexpected")
	ok1 = awssl.Succeed(Name="Success1")

	# Construct comparisons
	gt5 = awssl.Comparison(Variable="$.myValue", Comparator="NumericGreaterThan", Value=5)
	lt3 = awssl.Comparison(Variable="$.myValue", Comparator="NumericLessThan", Value=3)
	is3 = awssl.Comparison(Variable="$.myValue", Comparator="NumericEquals", Value=3)
	is4 = awssl.Comparison(Variable="$.myValue", Comparator="NumericEquals", Value=4)

	# Construct rules
	gt5orlt3 = awssl.OrChoiceRule(ComparisonList=[gt5, lt3], NextState=fail1)
	in3or4 = awssl.OrChoiceRule(ComparisonList=[is3, is4], NextState=ok1)

	# Construct states
	c1 = awssl.Choice(Name="Choice1", ChoiceList=[gt5orlt3, in3or4], Default=fail2)
	s1 = awssl.Pass(Name="Pass1", NextState=c1)

	# Construct state machine
	return awssl.StateMachine(Comment="This is a Choice test", StartState=s1)

def example_three():
	# Termination states
	f1 = awssl.Fail(
		Name="Fail1",
		ErrorName="Catch-All",
		ErrorCause="Unexpected error")

	# Catchers
	c1 = awssl.Catcher(
		ErrorNameList=[ "States.ALL"],
		NextState=f1)

	# Construct states
	s1 = awssl.Task(Name="Task1",
			Comment="This is a test task",
			ResourceArn="some-url",
			TimeoutSeconds=20,
			EndState=True,
			CatcherList=[c1])

	# Construct state machine
	return awssl.StateMachine(Comment="This is a Task test", StartState=s1)

def example_four():
	def create_branch(suffix):
		# Creates states for Parallel branches
		return awssl.Pass(
			Comment="This is an example of a state in branch {}".format(suffix),
			Name="Pass1-{}".format(suffix),
			EndState=True)

	# Construct main states
	BRANCH_COUNT = 2
	p1 = awssl.Parallel(
		Comment="This is a Parallel with {} branches".format(BRANCH_COUNT),
		Name="Parallel1",
		BranchList=[ create_branch(i) for i in range(0, BRANCH_COUNT) ],
		EndState=True)

	# Construct state machine
	return awssl.StateMachine(Comment="This is a Parallel test", StartState=p1)

def example_five(concatenator_lambda_arn):
	BRANCH_COUNT = 2
	NEST_COUNT = 3

	def get_suffix():
		from uuid import uuid4
		return str(uuid4())

	def create_concatenator(concatenator_lambda_arn):
		""" Merges a list of lists containing objects to a list containing objects

		The Lambda function invoked by the Task should look like this:

		def lambda_handler(event, context):
		    result = []
    		for l in event:
        		result = result + l
    		return result

		"""
		return awssl.Task(
			Comment="Concatenate results",
			Name="Concat-{}".format(get_suffix()),
			ResourceArn=concatenator_lambda_arn,
			EndState=True)

	def create_branch():
		# Creates states for Parallel branches
		suffix = get_suffix()
		return awssl.Pass(
			Comment="This is an example of a state in branch {}".format(suffix),
			Name="Pass1-{}".format(suffix),
			ResultAsJSON={"Value": suffix},
			OutputPath="$.Value",
			EndState=True)

	def created_nested_parallel(nest_level, branch, concatenator_lambda_arn):
		branch_list = []
		end_state = False
		next_state = None
		if nest_level == 0:
			branch_list = [ create_branch() for i in range(0, BRANCH_COUNT) ]
			end_state = True
		else:
			branch_list = [ created_nested_parallel(nest_level-1, i, concatenator_lambda_arn) for i in range(0, BRANCH_COUNT) ]
			next_state = create_concatenator(concatenator_lambda_arn)

		return awssl.Parallel(
			Comment="This is a Parallel at level {}".format(nest_level),
			Name="Parallel-{}".format(get_suffix()),
			BranchList=branch_list,
			EndState=end_state,
			NextState=next_state)


	# Construct main states
	p1 = awssl.Parallel(
		Comment="This is a Parallel with {} branches".format(BRANCH_COUNT),
		Name="Parallel1",
		BranchList=[ created_nested_parallel(NEST_COUNT-1, i, concatenator_lambda_arn) for i in range(0, BRANCH_COUNT) ],
		EndState=False,
		NextState=create_concatenator(concatenator_lambda_arn))

	# Construct state machine
	return awssl.StateMachine(Comment="This is a Parallel test", StartState=p1)

if __name__ == "__main__":
	sm = example_five("some arn")
	sm.validate()
	print sm

