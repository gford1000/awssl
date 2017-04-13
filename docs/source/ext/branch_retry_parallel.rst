BranchRetryParallel State
*************************

The ``BranchRetryParallel`` class extends the ``Parallel`` state.

``Parallel`` supports retrying the state if one or more of its branches generates an error that is included in the ``Retrier`` list.  This class extends this behaviour, allowing the branches to define errors that can be retried before the whole state is retried.

This extension can ensure that an intermittent failure on a single branch does not trigger significant unnecessary reprocessing of the successful branches.

For more details on ``Parallel``, see the `AWS documentation <http://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-parallel-state.html>`_.

.. automodule:: awssl.ext

.. autoclass:: BranchRetryParallel
   :members:

