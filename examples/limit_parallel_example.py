import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import awssl
import awssl.ext

def limit_parallel_example(iterations, max_concurrency):

	# Declare the Arns for the Lambda functions required by awssl.ext.For
	awssl.ext.set_ext_arns(
		ForInitializer="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME", 
		ForExtractor="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME", 
		ForConsolidator="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME", 
		ForFinalizer="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		ForFinalizerParallelIterations="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME",
		LimitedParallelConsolidator="arn:aws:lambda:REGION:ACCOUNT_ID:function:FUNCTION_NAME")

	# Create the branch of concurrent processing to be performed - in this case extraction of the iteration value
	p = awssl.Pass(Name="Dummy", EndState=True, OutputPath="$.iteration.Iteration")

	# Sometimes we want to throttle concurrent processing - for example to prevent Lambda function throttling
	# awssl.ext.LimitedParallel can limit the number of concurrent branches being processed at any given time
	parallel = awssl.ext.LimitedParallel(
		Name="LimitedParallel",
		EndState=True,
		Iterations=iterations,
		IteratorPath="$.iteration",
		MaxConcurrency=max_concurrency,
		BranchState=p)

	# Construct state machine
	sm = awssl.StateMachine(Comment="This is a test")
	sm.set_start_state(parallel)
	return sm


if __name__ == "__main__":
	sm = limit_parallel_example(25, 7)
	print sm

