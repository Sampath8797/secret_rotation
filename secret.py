import json
import boto3
import base64
import os
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    secret_name = os.environ.get('SECRET_NAME')
    key_to_update = os.environ.get('KEY')
    
    try:
        client = boto3.client("secretsmanager")
        get_secret_response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in get_secret_response:
            secret = json.loads(get_secret_response["SecretString"])
        else:
            raise ClientError("Secret Not Found", "SecretString missing in response")
    except ClientError as error:
        print(f"Error getting secret: {error}")
        return {
            "statuscode": 500,
            "body": json.dumps({"message": f"Error getting secret: {error}"}),
        }
    
    random_string = base64.base64encode(os.urandom(16)).decode("utf-8")
    
    if key_to_update in secret:
        secret[key_to_update] = random_string
        updated_secret_json = json.dumps(secret)
    else:
        print(f"Key '{key_to_update}' not found in secret")
        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": f"Key '{key_to_update}' noty found in secret"}
            ),
        }
    try:
         client.put_secret_value(SecretId=secret_name, SecretString=updated_secret_json)
         print("Secret updated")
         return {
             "statusCode": 200,
             "body": json.dumps({"message": "Secret updated"}),
         }
    except ClientError as error:
        print(f"Error updating secret: {error}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error updating secret: {error}"}),
        }