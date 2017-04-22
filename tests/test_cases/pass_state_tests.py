def register_tests():
	return [
		{
			"Name": "Test1",
			"Func": test1,	
			"ResultFileName": "./test_results/pass/test1.json"
		},
		{
			"Name": "Test2",
			"Func": test2,	
			"ResultFileName": "./test_results/pass/test2.json"
		}
	]

def test1():
	import awssl

	# Construct states
	hello_world = awssl.Pass(
		Name="HelloWorld",
		ResultAsJSON={"Hello": "World!"},
		EndState=True)

	# Construct state machine
	return awssl.StateMachine(
		Comment="A Hello World example of the Amazon States Language using a Pass state",
		StartState=hello_world)

def test2():
	import awssl

	# Construct states
	hello_world = awssl.Pass(
		Name="HelloWorld",
		EndState=True)

	# Construct state machine
	return awssl.StateMachine(
		Comment="A Hello World example of the Amazon States Language using a Pass state",
		StartState=hello_world)
