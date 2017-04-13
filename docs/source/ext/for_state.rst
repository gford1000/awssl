Extension: For State
********************

The ``For`` state provides a "for" loop, from a starting value to an ending value, incrementing via a defined step.  

The ``For`` state allows a single branch to be executed multiple times, either sequentially or concurrently.  Each execution is supplied the value of 
the iterator, at a location that can be specified by the ``IteratorPath`` argument.

One use case for this class occurs where processing will exceed the maximum execution time for an AWS Lambda (currently 300 seconds), but can be efficiently partitioned.  The ``For`` state then allows processing to be handled in AWS Lambda rather than having to create and maintain an ``Activity``.

.. automodule:: awssl.ext

.. autoclass:: For
   :members:

