import json
import boto3
import uuid
import pickle
import io
from urllib.parse import unquote_plus
from pprint import pprint


def lambda_handler(event, context):
    print('-------------- file uploaded ----------------')
    print(event)

    public_bucket = 'xiiot-demo'
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('xiiot-demo')

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        pickle_path = f'/tmp/{key}'
        s3.download_file(bucket, key, pickle_path)
        print(f'downloaded pickle file from S3 {bucket}/{key}')

        payload = pickle.load(open(pickle_path, 'rb'))
        video_file = f'/tmp/{payload["video_filename"]}'
        with open(video_file, 'wb') as file:
            file.write(payload['video_content'])
            file.close()

        s3.upload_file(video_file, public_bucket, payload['video_filename'])
        print(f'Uploaded file to S3 {public_bucket}/{payload["video_filename"]}')

        response = table.update_item(
            Key={'id': payload['id']},
            UpdateExpression='set video_url=:v',
            ExpressionAttributeValues={':v': f'https://xiiot-demo.s3-us-west-2.amazonaws.com/{payload["video_filename"]}'}
        )
        print('DynamoDB record updated')
        pprint(response, sort_dicts=False)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
