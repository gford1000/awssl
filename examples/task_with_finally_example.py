import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import awssl
import awssl.ext

def task_with_finally_example():

	finally_state = awssl.Pass(
		Name="Finally",
		Comment="This is the branch to execute as a 'finally' statement to the Task",
		ResultAsJSON={"Finally": "Completed"},
		EndState=True)

	catch_state_0 = awssl.Pass(
		Name="Catcher-MyError",
		Comment="This is the branch to execute when a 'MyError' error is caught",
		ResultAsJSON={"Caught": "Error"},
		EndState=True)

	catch_state_1 = awssl.Pass(
		Name="Catcher-All",
		Comment="This is the branch to execute any other error is caught",
		ResultAsJSON={"Caught": "Error"},
		EndState=True)

	# Construct states
	hello_world = awssl.ext.TaskWithFinally(
		Name="HelloWorld",
		Comment="This is the actual Task to be executed",
		ResourceArn="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		FinallyState=finally_state,
		CatcherList=[
			awssl.Catcher(ErrorNameList=["MyError"], NextState=catch_state_0),
			awssl.Catcher(ErrorNameList=["States.ALL"], NextState=catch_state_1)
		],
		EndState=True)

	# Construct state machine
	return awssl.StateMachine(
		Comment="A Task finally example, where the finally branch is executed both after successful completion, and before any Catchers are triggered when an error occurs",
		StartState=hello_world)

if __name__ == "__main__":
	sm = task_with_finally_example()
	print sm

