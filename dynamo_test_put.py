import boto3
import uuid
import time

def key():
    return str(uuid.uuid4())

def timestamp():
    return int(time.time())

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("vida-version")
print(table.creation_date_time)

table.put_item(Item = {
    'id': "current_version",
    'version': '1.30.8'
})
