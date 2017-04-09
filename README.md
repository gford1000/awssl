# awssl

Python 2.7 package to construct ASL compliant JSON that define State Machines
for AWS Step Functions.

## Example

```python
from awssl import Pass, StateMachine

s = Pass(
		Comment="This is an example of a state in branch",
		Name="Pass1",
		ResultAsJSON={"Value": 1234},
		OutputPath="$.Value",
		EndState=True)

sm = StateMachine(
		Comment="This is an instance of a State Machine",
		StartState=s)

print sm

```

The `ext` package provides more complex processing state types, such as `For` and `LimitedParallel`, by combining 
the core state types appropriately.  These require particular Lambda functions to be present, which can be 
installed by creating a CloudFormation stack - see the [script](cloudformation/awssl_ext.cform) for details.

```python

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
sm = awssl.StateMachine(Comment="This is a test", StartState=parallel)
print sm

```

## Installation

To install, use `pip install awssl`.

## Documentation

Documentation is available at [read the docs](http://awssl.readthedocs.io/en/latest/index.html).

## Coverage

The package provides support for version 1.0 of [Amazon Step Language](https://states-language.net/spec.html).

No checking is performed for correctness of Paths - these are expected to be 
valid [JsonPath](https://github.com/json-path/JsonPath), as implemented by the
[Step Functions](http://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-paths.html).


## Licence

This project is released under the MIT license. See [LICENSE](LICENSE) for details.
