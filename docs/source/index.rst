AWS Step Function State Language Builder (awssl)
================================================

The awssl package generates JSON that is compliant with the Amazon State Language (ASL), declaring State Machines for use in the AWS Step Function service.

    import awssl
    
    hello_world = awssl.Pass(
        Name="HelloWorld",
        ResultAsJSON={"Hello": "World!"},
        EndState=True)
    
    sm = awssl.StateMachine(
        Comment="A Hello World example of the Amazon States Language using a Pass state",
        StartState=hello_world)
    
    print sm

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
