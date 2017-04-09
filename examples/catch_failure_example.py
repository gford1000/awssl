import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import awssl

def catch_failure_example():
	# Fallback states
	reserved_type_fallback = awssl.Pass(
		Name="ReservedTypeFallback",
		ResultAsJSON={"msg": "This is a fallback from a reserved error code"},
		OutputPath="$.msg",
		EndState=True)

	catch_all_fallback = awssl.Pass(
		Name="CatchAllFallback",
		ResultAsJSON={"msg": "This is a fallback from a reserved error code"},
		OutputPath="$.msg",
		EndState=True)

	custom_error_fallback = awssl.Pass(
		Name="CustomErrorFallback",
		ResultAsJSON={"msg": "This is a fallback from a custom lambda function exception"},
		OutputPath="$.msg",
		EndState=True)

	# Catchers for the HelloWorld task state
	states_all_catcher = awssl.Catcher(
		ErrorNameList=["States.ALL"],
		NextState=catch_all_fallback)

	reserved_type_catcher = awssl.Catcher(
		ErrorNameList=["States.TaskFailed"],
		NextState=reserved_type_fallback)

	custom_error_catcher = awssl.Catcher(
		ErrorNameList=["CustomError"],
		NextState=custom_error_fallback)

	# Construct states
	hello_world = awssl.Task(
		Name="HelloWorld",
		ResourceArn="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		EndState=True,
		CatcherList=[custom_error_catcher, reserved_type_catcher, states_all_catcher])

	# Construct state machine
	return awssl.StateMachine(
		Comment="A Catch example of the Amazon States Language using an AWS Lambda Function",
		StartState=hello_world)

if __name__ == "__main__":
	sm = catch_failure_example()
	print sm

