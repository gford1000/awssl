import awssl

def choice_example():

	# Construct states for each choice 
	default = awssl.Fail(
		Name="Default",
		ErrorCause="No Matches!")

	next_state = awssl.Task(
		Name="NextState",
		ResourceArn="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		EndState=True)

	first_match_state = awssl.Task(
		Name="FirstMatchState",
		ResourceArn="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		EndState=False,
		NextState=next_state)

	second_match_state = awssl.Task(
		Name="SecondMatchState",
		ResourceArn="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		EndState=False,
		NextState=next_state)


	# Construct Choice Rules
	first_rule = awssl.ChoiceRule(
		Comparison=awssl.Comparison(
			Variable="$.foo",
			Comparator="NumericEquals",
			Value=1),
		NextState=first_match_state)

	second_rule = awssl.ChoiceRule(
		Comparison=awssl.Comparison(
			Variable="$.foo",
			Comparator="NumericEquals",
			Value=2),
		NextState=second_match_state)

	# Construct states for main branch
	choice_state = awssl.Choice(
		Name="ChoiceState",
		ChoiceList=[first_rule, second_rule],
		Default=default)

	first_state = awssl.Task(
		Name="FirstState",
		ResourceArn="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		EndState=False,
		NextState=choice_state)

	# Construct state machine
	return awssl.StateMachine(
		Comment="An example of the Amazon States Language using a choice state.",
		StartState=first_state)

if __name__ == "__main__":
	sm = choice_example()
	print sm

