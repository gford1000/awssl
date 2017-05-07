import boto3
from json import loads, dumps
from uuid import uuid4

_S3_BUCKET="1a1aaf8a-a15a-4b74-b2ba-817834541988"

def extract_event_details(event):
    message = event.get('Records', [{}])[0].get('Sns', {}).get('Message', None)
    if message == None:
        raise Exception("Message does not exist in event")
    message = loads(message)
    task_token = message.get('TaskToken', None)
    if task_token == None:
        raise Exception("TaskToken not present in event")
    input_data = message.get('InputData', None)
    if input_data == None:
        raise Exception("InputData not present in event")
    branch_arn = input_data.pop('BranchArn', None)
    if branch_arn == None:
        raise Exception("BranchArn not present in the provided InputData")
    activity_arn = message.get('ActivityArn', None)
    if activity_arn == None:
        raise Exception("ActivityArn not present in event")
    return (task_token, input_data, branch_arn, activity_arn)

def start_execution(branch_arn, input_data):
    print("Starting execution of {} with inputs {}".format(branch_arn, input_data))
    try:
        execution_name = str(uuid4())
        
        client = boto3.client('stepfunctions')
        resp = client.start_execution(
            stateMachineArn=branch_arn, 
            name=execution_name,
            input=dumps(input_data))
        
        print("Launched successfully {}".format(resp["executionArn"]))
        return { "Name": execution_name, "ExecutionArn": resp["executionArn"] }
    except Exception as e:
        raise Exception("Error starting Branch {}: {}".format(branch_arn, e))

def save_s3_file(s3_file_content):
    try:
        key = "Active/{}".format(s3_file_content["ExecutionArn"])
        print("Saving execution details to S3: {}:{}".format(_S3_BUCKET, key))
        client = boto3.client('s3')
        resp = client.put_object(
            Bucket=_S3_BUCKET,
            Key=key,
            Body=bytearray(dumps(s3_file_content)),
            ContentType="application/json")
        print("Save successful")
    except Exception as e:
        raise Exception("Error saving execution details {}: {}".format(s3_file_content, e))

def process_task(task_token, input_data, branch_arn, activity_arn):
    s3_file_content = { "TaskToken": task_token, "ActivityArn": activity_arn, "InputData": input_data }
    resp = start_execution(branch_arn, input_data)
    s3_file_content["Name"] = resp["Name"]
    s3_file_content["ExecutionArn"] = resp["ExecutionArn"]
    save_s3_file(s3_file_content)

def lambda_handler(event, context):
    try:
        print("Processing event: {}".format(event))
        (task_token, input_data, branch_arn, activity_arn) = extract_event_details(event)
        process_task(task_token, input_data, branch_arn, activity_arn)
        print("Processing completed")
    except Exception as e:
        print("Unexpected error in processing:\n\t{}".format(e))
