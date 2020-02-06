import json
import boto3
import os
import random
import string


def random_string():
    """Generate a random string for dynamodb table id"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

def get_table(table):
    """Get dynamoDB table"""
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(table)


def get_item(table, query):
    """
    Retrieve and item from the table
    Params:
    -table: table name
    -query: query with partition key: {'id': 'abbcs'}
    """
    t = get_table(table)
    return t.get_item(Key=query)


def put_item_in_table(item, table):
    """
    Put a new item in the table
    Params:
    -item: item that will be added on the table
    -table: table name
    """
    t = get_table(table)
    return t.put_item(Item=item)


def scan_table(table):
    """
    Retrieves all table items
    Params:
    -table: table name
    """
    t = get_table(table)
    # Retrieve the item from the db.
    return t.scan()


def delete_item(table, query):
    """
    Deletes an item from a table
    Params:
    -table: table name
    -query: query with partition key: {'id': 'abbcs'}
    """
    t = get_table(table)
    return t.delete_item(
        Key=query
    )


def update_db_item(query, table, item_key, item_value):
    """
    Update an item from a table
    Params:
    -query: query with partition key: {'id': 'abbcs'}
    -table: table name
    -item_key: new column 
    -item_value: value from new column
    """
    t = get_table(table)

    return t.update_item(
        Key=query,
        UpdateExpression=f"SET {item_key} = :item_value",
        ExpressionAttributeValues={':item_value': item_value},
        ReturnValues="ALL_NEW"
    )


def lambda_handler(event, context):
    """Lambda function"""
    http_method = event['httpMethod']
    table_name = os.environ.get('INFO_TABLE', 'def')
    if http_method == 'GET':   
        results = scan_table(table_name)['Items']    
        if results:
            return {
                'body': json.dumps(results),
                'statusCode': 200
            }
        else:
           return {
                'body': json.dumps('No content'),
                'statusCode': 204
            }
    elif http_method == 'PUT':
        if event['body']:
            body = json.loads(event['body'])
        elif event['queryStringParameters']:
            body = event['queryStringParameters']
        else:
            return {
                'body': json.dumps('KeyError no message'),
                'statusCode': 404
            }
        if 'message' in body:
            message = body['message']
            results = scan_table(table_name)['Items']
            if results:
                print(results)
                for i in results:
                    if message == i['message']:
                        #message already exists
                        query = {'id': i['id']}
                        item = get_item(table_name, query)
                        if 'Item' in item:
                            update_db_item(query, table_name, 'message', body['message'])
                            return {
                                'body': json.dumps('Successfully updated'),
                                'statusCode': 200
                            }
            #message doesn´t exists  
            new_item = {'id': random_string(), 'message': body['message']}
            put_item_in_table(new_item, table_name)
            return {
                'body': json.dumps('Successfully created'),
                'statusCode': 201
            }
        else:
            return {
                'body': json.dumps('KeyError no message'),
                'statusCode': 404
            }
    elif http_method == 'DELETE':
        if event['body']:
            body = json.loads(event['body'])
        elif event['queryStringParameters']:
            body = event['queryStringParameters']
        else:
            return {
                'body': json.dumps('KeyError no message'),
                'statusCode': 404
            }
        if 'message' in body:
            message = body['message']
            results = scan_table(table_name)['Items']
            if results:
                for i in results:
                    if message == i['message']:
                        #message already exists
                        query = {'id': i['id']}
                        item = get_item(table_name, query)
                        if 'Item' in item:
                            delete_item(table_name, query)
                            return {
                                'body': json.dumps('Successfully deleted'),
                                'statusCode': 200
                            }
                return {
                    'body': json.dumps('No content'),
                    'statusCode': 204
                }
