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
