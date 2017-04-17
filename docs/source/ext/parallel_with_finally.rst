Extension: ParallelWithFinally State
************************************

The ``ParallelWithFinally`` state extends the ``Parallel`` state to provide a "finally" branch, which will be executed both for successful completion of the branches in the state, but also whenever a ``Catcher`` is triggered due to an error in processing.

The "finally" branch will always be executed prior to the ``NextState`` of either the parallel state or the catcher.

No results are returned by the "finally" branch.

.. automodule:: awssl.ext

.. autoclass:: ParallelWithFinally
   :members:

