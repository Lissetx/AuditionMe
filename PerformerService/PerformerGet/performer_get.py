import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
from os import getenv

region_name = getenv('APP_REGION')
performer_table = boto3.resource('dynamodb', region_name=region_name).Table('Performer')

def lambda_handler(event, context):
    if "pathParameters" not in event or "queryStringParameters" not in event:
      return response(200, performer_table.scan()["Items"])
    
    path = event["pathParameters"]
    #get by id
    if path is not None and "id" in path:
        output = performer_table.get_item(Key={"Id":path["id"]})["Item"]
        return response(200, output)
    
    params = event["queryStringParameters"]
    #get by name search
    if params is not None and "name" in params:
        output = performer_table.scan(FilterExpression=Attr("Name").eq(params["name"]))["Items"]
        response(200, output)
    
    return response(200, performer_table.scan()["Items"])


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json"
            },
        "body": json.dumps(body)
    }