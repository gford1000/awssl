Initialisation of Ext State Types
*********************************

The ``For`` and ``LimitedParallel`` extension states require data manipulation between states, and this is supported by a series of Lambda functions.

The Lambda function themselves can be found in the `github repo <https://github.com/gford1000/awssl/tree/master/lambda>`_, and they have been incorporated into an `AWS CloudFormation script <https://github.com/gford1000/awssl/blob/master/cloudformation/awssl_ext.cform>`_ so that they can be easily added to the AWS account / region that the AWS Step Function state machines will be executed.

Once created, the Arns of the Lambda functions must be passed to the awssl package; this is the purpose of these functions.

.. automodule:: awssl.ext

.. autofunction:: get_ext_arn

.. autofunction:: get_ext_arn_keys

.. autofunction:: set_ext_arns

