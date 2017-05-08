import boto3
from uuid import uuid4

_LIST_COUNT=250

def extract_event_details(event):
    branch_arn = event.get('BranchArn', None)
    if not branch_arn:
        raise Exception("BranchArn key does not exist in event")
    return (branch_arn)

def check_existence(branch_arn):
    def find_in_list(arn_list, arn):
        for item in arn_list:
            if item.get('stateMachineArn', None) == arn:
                return True
        return False

    try:
        client = boto3.client('stepfunctions')

        resp = client.list_state_machines(maxResults=_LIST_COUNT)
        if find_in_list(resp.get('stateMachines', []), branch_arn):
            return

        while resp.get('nextToken', None):
            resp = client.list_state_machines(
                maxResults=_LIST_COUNT,
                nextToken=resp['nextToken'])
            if find_in_list(resp.get('stateMachines', []), branch_arn):
                return
        
        raise Exception("StateMachine not found")
        
    except Exception as e:
        raise Exception("Unexpected error checking existence of {}: {}".format(branch_arn, e))

def lambda_handler(event, context):
    class ValidateStateMachineException(Exception):
        pass
    
    print("Processing started for event: {}".format(event))
    try:
        # Extract details from the event
        (branch_arn) = extract_event_details(event)
        
        # Validate the StateMachine exists
        check_existence(branch_arn)
        
        # StateMachine exists - provide a unique id for this execution of it
        return { "ExecutionId" : str(uuid4()) }
    except Exception as e:
        raise ValidateStateMachineException("Error processing: {}".format(e))
    finally:
        print("Processing completed")
