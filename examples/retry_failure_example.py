import awssl

def retry_failure_example():

	retrier1 = awssl.Retrier(
		ErrorNameList=["CustomError"],
		IntervalSeconds=1,
		MaxAttempts=2,
		BackoffRate=2.0)

	states_all_retrier = awssl.Retrier(
		ErrorNameList=["States.ALL"],
		IntervalSeconds=5,
		MaxAttempts=5,
		BackoffRate=2.0)

	# Construct states
	hello_world = awssl.Task(
		Name="HelloWorld",
		ResourceArn="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		EndState=True,
		RetryList=[retrier1, states_all_retrier])

	# Construct state machine
	return awssl.StateMachine(
		Comment="A Retry example of the Amazon States Language using an AWS Lambda Function",
		StartState=hello_world)

if __name__ == "__main__":
	sm = retry_failure_example()
	print sm

