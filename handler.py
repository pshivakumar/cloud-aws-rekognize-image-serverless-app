import boto3

def lambda_handler(event, context):
    rekognition = boto3.client('rekognition')
    
    print(f"Event structure is - {event}")
    
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
            print(f"Label: {label['Name']}, Confidence: {label['Confidence']}")
        
        return {
            'statusCode': 200,
            'body': 'Image recognition complete.'
        }
    else:
        # Handle the case when 'Records' is not present in the event structure
        print("No 'Records' found in the event structure.")
        return {
            'statusCode': 400,
            'body': 'Invalid event structure.'
        }


    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
