import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import awssl

def hello_world_example():

	# Construct states
	hello_world = awssl.Pass(
		Name="HelloWorld",
		ResultAsJSON={"Hello": "World!"},
		EndState=True)

	# Construct state machine
	return awssl.StateMachine(
		Comment="A Hello World example of the Amazon States Language using a Pass state",
		StartState=hello_world)

if __name__ == "__main__":
	sm = hello_world_example()
	print sm

