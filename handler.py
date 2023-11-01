import boto3
import logging
import os

def init_logging():   
    # Configure the logger to use the specified log group
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


def lambda_handler(event, context):
    logger = init_logging()
    rekognition = boto3.client('rekognition')
    
    logger.info(f"Event structure is - {event}")
    
    # Check if the event structure includes 'Records'
    if 'Records' in event:
        s3_bucket = event['Records'][0]['s3']['bucket']['name']
        s3_object = event['Records'][0]['s3']['object']['key']

        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': s3_bucket,
                    'Name': s3_object
                }
            }
        )

        for label in response['Labels']:
            logger.info(f"Label: {label['Name']}, Confidence: {label['Confidence']}")
        
        return {
            'statusCode': 200,
            'body': 'Image recognition complete.'
        }
    else:
        # Handle the case when 'Records' is not present in the event structure
        logger.info("No 'Records' found in the event structure.")
        return {
            'statusCode': 400,
            'body': 'Invalid event structure.'
        }
