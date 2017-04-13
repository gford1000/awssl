AWS Step Function State Language Builder (awssl)
================================================

The awssl package generates JSON that is compliant with the `Amazon States Language (ASL) <https://states-language.net/spec.html>`_, declaring State Machines for use in the AWS Step Function service::

	import awssl

	hello_world = awssl.Pass(
		Name="HelloWorld",
		ResultAsJSON={"Hello": "World!"},
		EndState=True)

	sm = awssl.StateMachine(
		Comment="A Hello World example of the Amazon States Language using a Pass state",
		StartState=hello_world)

	print sm

Which creates the following JSON::

	{
	    "Comment": "A Hello World example of the Amazon States Language using a Pass state", 
	    "StartAt": "HelloWorld", 
	    "States": {
	        "HelloWorld": {
	            "Comment": "", 
	            "End": true, 
	            "InputPath": "$", 
	            "OutputPath": "$", 
	            "Result": {
	                "Hello": "World!"
	            }, 
	            "ResultPath": "$", 
	            "Type": "Pass"
	        }
	    }, 
	    "Version": "1.0"
	}

For more examples see the `awssl git repo <https://github.com/gford1000/awssl>`_ on github.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   catcher
   fail_state
   pass_state
   parallel_state
   retrier
   state_machine
   succeed_state
   task_state
   wait_state

   ext/branch_retry_parallel
   ext/for_state
   ext/limited_parallel
   ext/arn_funcs



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
