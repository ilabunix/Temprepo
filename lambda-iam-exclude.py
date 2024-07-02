import os
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    try:
        # Define a list of users to ignore
        ignore_list = ['UserToIgnore1', 'UserToIgnore2', 'ServiceAccount1']

        # Extract user identity from the event
        user_identity = event.get('detail', {}).get('userIdentity', {}).get('userName', 'N/A')

        # Check if the user is in the ignore list
        if user_identity in ignore_list:
            logger.info(f"Event by user {user_identity} is ignored.")
            return {
                'statusCode': 200,
                'body': json.dumps(f"Event by user {user_identity} ignored.")
            }

        # Simulated event details (replace with actual data from your event)
        event_name = "CreateUser"
        event_time = "2024-01-01T12:00:00Z"
        source_ip = "192.0.2.1"
        userAgent = "AWS CLI v2.0"
        error_message = "None"
        error_code = "None"

        # Create a formatted message
        message = (
            f"**Event Details:**\n\n"
            f"**Event Name:** {event_name}\n"
            f"**User Identity:** {user_identity}\n"
            f"**Event Time:** {event_time}\n"
            f"**Source IP:** {source_ip}\n"
            f"**User Agent:** {userAgent}\n"
            f"**Error Message:** {error_message}\n"
            f"**Error Code:** {error_code}\n"
        )

        subject = "IAM Activity Notification"

        # Publish to SNS
        response = sns_client.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Message=message,
            Subject=subject
        )
        logger.info(f"Message published to SNS topic {os.environ['SNS_TOPIC_ARN']}")

    except Exception as e:
        logger.error(f"Failed to publish message: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps(f"Failed to publish message: {str(e)}")
        }

    return {
        'statusCode': 200,
        'body': json.dumps("Message successfully sent to SNS")
    }