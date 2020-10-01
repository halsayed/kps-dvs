import boto3
from config import Config, log


dynamodb = boto3.resource('dynamodb')
item_key = lambda x: x['location'] if x.get('location') else 'undefined'
table = dynamodb.Table(Config.DYNAMO_TABLE)
log.info(f'Table creation time: {table.creation_date_time}')
log.info(f'Table items count: {table.item_count}')

dynamoStream = boto3.client('dynamodbstreams')
next_shard_iterator = None


def list_all_records(limit=100, search=None):
    response = table.scan(Limit=limit)

    result = {}
    for item in response['Items']:
        if search and search.lower() not in item['value'].lower():
            continue
        key = item_key(item)
        if key in result.keys():
            result[key].append(item)
        else:
            result[key] = [item]

    result = sort_locations(result)

    return result


def sort_locations(original_list):
    locations = list(original_list.keys())
    locations.sort()
    sorted_list = {}
    for location in locations:
        sorted_list[location] = sort_cards_by_time(original_list[location])

    return sorted_list


def sort_cards_by_time(original_cards):
    return sorted(original_cards, key=lambda k: k['trigger_time'], reverse=True)


def get_latest_stream_arn():
    streams = dynamoStream.list_streams(TableName=Config.DYNAMO_TABLE)
    sorted_streams = sorted(streams['Streams'], key=lambda k: k['StreamLabel'], reverse=True)
    return sorted_streams[0]['StreamArn']


def get_last_iterator():
    global next_shard_iterator

    if next_shard_iterator:
        return next_shard_iterator
    else:
        stream_arn = get_latest_stream_arn()
        stream_details = dynamoStream.describe_stream(StreamArn=stream_arn)
        shard_id = stream_details['StreamDescription']['Shards'][0]['ShardId']
        return dynamoStream.get_shard_iterator(StreamArn=stream_arn,
                                               ShardId=shard_id,
                                               ShardIteratorType='LATEST')['ShardIterator']


def read_stream_records():
    global next_shard_iterator

    shard_iterator = get_last_iterator()
    result = dynamoStream.get_records(ShardIterator=shard_iterator, Limit=100)
    next_shard_iterator = result.get('NextShardIterator')
    records_list = []
    for record in result['Records']:
        formatted_record = {'eventName': record['eventName']}
        new_image = record['dynamodb']['NewImage']
        for key, value in new_image.items():
            value_type = list(value.keys())[0]
            if value_type == 'N':
                formatted_record[key] = int(value[value_type])
            else:
                formatted_record[key] = value[value_type]
        records_list.append(formatted_record)

    inserts = []
    updates = []
    for record in records_list:
        print(record)
        if record['eventName'] == 'INSERT':
            inserts.append(record)
            log.info(f'record inserted: {record["id"]}')
        elif record['eventName'] == 'MODIFY':
            updates.append(record)
            log.info(f'record updated: {record["id"]}')

    location_sorted = {}
    if inserts:
        for item in inserts:
            key = item_key(item)
            if key in location_sorted.keys():
                location_sorted[key].append(item)
            else:
                location_sorted[key] = [item]

    return location_sorted, updates
