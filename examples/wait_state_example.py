import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import awssl

def wait_state_example():

	# Construct states
	final_state = awssl.Task(
		Name="FinalState",
		EndState=True,
		ResourceArn="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME")

	wait_using_seconds_path = awssl.Wait(
		Name="wait_using_seconds_path",
		NextState=final_state,
		WaitForSecondsPath="$.expiryseconds")

	wait_using_timestamp_path = awssl.Wait(
		Name="wait_using_timestamp_path",
		NextState=wait_using_seconds_path,
		WaitUntilISO8601TimestampPath="$.expirydate")

	wait_using_timestamp = awssl.Wait(
		Name="wait_using_timestamp",
		NextState=wait_using_timestamp_path,
		WaitUntilISO8601Timestamp="2015-09-04T01:59:00Z")

	wait_using_seconds = awssl.Wait(
		Name="wait_using_second", 
		NextState=wait_using_timestamp, 
		WaitForSeconds=10)

	first_state = awssl.Task(
		Name="FirstState",
		ResourceArn="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		EndState=False,
		NextState=wait_using_seconds)

	# Construct state machine
	return awssl.StateMachine(
		Comment="An example of the Amazon States Language using wait states",
		StartState=first_state)

if __name__ == "__main__":
	sm = wait_state_example()
	print sm

