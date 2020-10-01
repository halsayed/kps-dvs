import json
import boto3


def lambda_handler(event, context):
    # TODO implement
    print('received a message from SQS -----------------')
    print(event)

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('xiiot-demo')

    for message in event['Records']:
        response = table.put_item(Item=json.loads(message['body']))
        print(f'Message inserted to dynamodb: {response}')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
