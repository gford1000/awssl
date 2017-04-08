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

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   state_machine



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
