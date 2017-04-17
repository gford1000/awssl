Extension: TaskWithFinally State
********************************

The ``TaskWithFinally`` state extends the ``Task`` state to provide a "finally" branch, which will be executed both for successful completion of the task, but also whenever a ``Catcher`` is triggered due to an error in processing.

The "finally" branch will always be executed prior to the ``NextState`` of either the task or the catcher.

No results are returned by the "finally" branch.

.. automodule:: awssl.ext

.. autoclass:: TaskWithFinally
   :members:

