import boto3
from botocore.config import Config
import json

my_config = Config(region_name='us-west-2')
table_name = 'xiiot-demo'


# DB stream test ...
client = boto3.client('dynamodbstreams')
response = client.describe_stream(StreamArn='arn:aws:dynamodb:us-west-2:564757554894:table/xiiot-demo/stream/2020-09-23T10:05:06.104',)
print(response)


# # DynamoDB test
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(table_name)
# print(f'Table creation time: {table.creation_date_time}')
# print(f'Table items count: {table.item_count}')
# response = table.scan(Limit=100)
#
# item_key = lambda x: x['location'] if x.get('location') else 'undefined'
#
# result = {}
# for item in response['Items']:
#     key = item_key(item)
#     if key in result.keys():
#         result[key].append(item)
#     else:
#         result[key] = [item]
#
# for location in result:
#     print(f'Location: {location}')
#     for entry in result[location]:
#         print(entry)
#     print('-----------------------------------\n')



