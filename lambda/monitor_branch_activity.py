import boto3
from botocore.config import Config
from datetime import datetime, timedelta
from json import loads, dumps

_LAMBDA_TIMEOUT=180
_READ_TIMEOUT=65
_POST_PROCESS_INTERVAL = 2

_WORKER_NAME="B3"
_SNS_TOPIC_ARN="arn:aws:sns:eu-west-1:665796216255:Blah"

def extract_event_details(event):
    activity_arn = event.get('ActivityArn', None)
    if not activity_arn:
        raise Exception("ActivityArn key does not exist in event")
    return (activity_arn)

def get_task(activity_arn):
    try:
        client = boto3.client('stepfunctions', config=Config(read_timeout=_READ_TIMEOUT))
        resp = client.get_activity_task(activityArn=activity_arn, workerName=_WORKER_NAME)
        task_token = resp.get('taskToken', '')
        if task_token:
            return (task_token, loads(resp['input']))
        else:
            return (None, None)
    except Exception as e:
        raise Exception("Error checking Activity '{}' for pending tasks: {}".format(activity_arn, e))

def dispatch_tasks(activity_arn, task_token, input_data):
    try:
        client = boto3.client('sns')
        resp = client.publish(
            TopicArn=_SNS_TOPIC_ARN,
            MessageStructure='json',
            Message=dumps({"default": dumps({ "ActivityArn": activity_arn, "TaskToken": task_token, "InputData": input_data }) } ) )
        print("Dispatched TaskToken '{}' to SNS Topic '{}'".format(task_token, _SNS_TOPIC_ARN))
    except Exception as e:
        raise Exception("Error dispatching task: {}".format(e))

def process_tasks(activity_arn):
    dend = datetime.now() + timedelta(0, _LAMBDA_TIMEOUT)
    while True:
        if datetime.now() + timedelta(0, _READ_TIMEOUT + _POST_PROCESS_INTERVAL) > dend:
            break
        (task_token, input_data) = get_task(activity_arn)
        if task_token:
            dispatch_tasks(activity_arn, task_token, input_data)

def lambda_handler(event, context):
    class ActivityMonitorException(Exception):
        pass
    
    try:
        (activity_arn) = extract_event_details(event)
        process_tasks(activity_arn)
    except Exception as e:
        raise ActivityMonitorException("Error processing: {}".format(e))
