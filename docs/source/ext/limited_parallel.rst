LimitedParallel State
*********************

The ``LimitedParallel`` class allows concurrent processing, across arbitrary invocations of the same branch, but limited by a maximum
number of concurrent executions.

This allows finer control over AWS Lambda invocations to avoid unexpected throttling by AWS Lambda (and associated timeouts, due to
exceeding the maximum number of Lambda concurrent executions per second.

For more details on ``Parallel``, see the `AWS documentation <http://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-parallel-state.html>`_.

.. automodule:: awssl.ext

.. autoclass:: LimitedParallel
   :members:

