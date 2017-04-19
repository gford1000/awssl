import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import awssl
import awssl.ext

def for_state_example():

	# Declare the Arns for the Lambda functions required by awssl.ext.For
	awssl.ext.set_ext_arns(
		ForInitializer="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME", 
		ForExtractor="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME", 
		ForConsolidator="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME", 
		ForFinalizer="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		ForFinalizerParallelIterations="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		LimitedParallelConsolidator="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME")

	# Create the branch processing to be performed - in this case extraction of the iteration value
	p = awssl.Pass(Name="Dummy", EndState=True, OutputPath="$.iteration.Iteration")

	r = awssl.Retrier(ErrorNameList=["States.ALL"])

	# Create 2 identical For loops - one where the branches are retryable, and one where they aren't
	s1 = awssl.ext.For(Name="For1", EndState=True,
		From=0, To=5, Step=1, BranchState=p, BranchRetryList=[r], ParallelIteration=True)

	s2 = awssl.ext.For(Name="For2", EndState=True,
		From=0, To=5, Step=1, BranchState=p, ParallelIteration=True)

	# Run the For loops in parallel, to demonstrate there is no interdependencies
	para = awssl.Parallel(
		Name="Parallel-Fors",
		BranchList=[s1,s2],
		EndState=True)

	# Construct state machine
	sm = awssl.StateMachine(Comment="This is a test")
	sm.set_start_state(para)
	return sm


if __name__ == "__main__":
	sm = for_state_example()
	print sm

