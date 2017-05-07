import boto3
from datetime import datetime, timedelta
from json import loads, dumps
from time import sleep

_SLEEP = 5
_LAMBDA_TIMEOUT=60
_S3_BUCKET="k19-branchs3bucket-1bq0zgaso93zd"
_S3_BUCKET="k22-branchs3bucket-1kk5rhiq8zrid"

def get_active_executions():
    active_keys = []
    
    try:
        print("Retrieving active executions")
        client = boto3.client('s3')
        resp = client.list_objects_v2(
            Bucket=_S3_BUCKET,
            Prefix="Active/")
        for key_info in resp.get("Contents", []):
            active_keys.append(key_info["Key"])
        while resp.get("IsTruncated", False):
            resp = client.list_objects_v2(
                Bucket=_S3_BUCKET,
                Prefix="Active/",
                ContinuationToken=resp["NextContinuationToken"])
            for key_info in resp["Contents"]:
                active_keys.append(key_info["Key"])
        print("{} executions found".format(len(active_keys)))
    except Exception as e:
        print("Error retrieving active tasks from {}: {}".format(_S3_BUCKET, e))
    
    return active_keys

def process_active_execution(key):
    try:
        
        # Load details of execution
        s3_client = boto3.client('s3')
        excution_data = {}
        resp = {}
        try:
            resp = s3_client.get_object(
                Bucket=_S3_BUCKET,
                Key=key)
            execution_data = loads(resp["Body"].read())
        except Exception as e:
            print("Caught error retrieving key {}: {}".format(key, e))
            return
        
        # Send heartbeat
        sf_client = boto3.client('stepfunctions')
        try:
            sf_client.send_task_heartbeat(taskToken=execution_data["TaskToken"])
        except Exception as e:
            print("Caught heartbeat exception: {}".format(e))
            
        # Check on StateMachine
        resp = sf_client.describe_execution(executionArn=execution_data["ExecutionArn"])
        if resp["status"] == "RUNNING":
            print("\tStill running")
            return
        
        if resp["status"] == "SUCCEEDED":
            print("\tBranch processing succesful")
            sf_client.send_task_success(
                taskToken=execution_data["TaskToken"],
                output=resp["output"])
        else:
            print("\tBranch processing failed:\n\t{}".format(resp["output"]))
            sf_client.send_task_failure(
                taskToken=execution_data["TaskToken"],
                error="Processing error",
                cause=resp["output"])
        
        execution_data["Status"] = resp["status"]
        execution_data["Output"] = resp["output"]
        
        # Move to archival
        archive_key = "Archive/{}".format("/".join(key.split("/")[1:]))
        print("Archiving execution to {}".format(archive_key))
        s3_client.put_object(
            Bucket=_S3_BUCKET,
            Key=archive_key,
            Body=bytearray(dumps(execution_data)),
            ContentType="application/json")
        
        # Delete active key
        try:
            s3_client.delete_object(
                Bucket=_S3_BUCKET,
                Key=key)
        except:
            pass

    except Exception as e:
        print("Error processing key {}: {}".format(key, e))

def process():
    print("Starting to monitor for execution completion")
    dend = datetime.now() + timedelta(0, _LAMBDA_TIMEOUT)
    while True:
        if datetime.now() + timedelta(0, 10) > dend:
            print("Insufficient time for monitor cycle - exiting")
            break
        for key in get_active_executions():
            print("Processing: {}".format(key))
            process_active_execution(key)
            print("Completed processing for: {}".format(key))
        sleep(_SLEEP)
    print("Ending monitoring for execution completion")

def lambda_handler(event, context):
    try:
        process()
    except Exception as e:
        print("Caught unexpected error during processing: {}".format(e))