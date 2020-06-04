import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("vida-version")
response = table.get_item()
print(response)
