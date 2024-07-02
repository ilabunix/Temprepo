import json
import boto3
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        sns_client = boto3.client('sns')
        sts_client = boto3.client('sts')
        iam_client = boto3.client('iam')

        # Get account alias
        account_id = sts_client.get_caller_identity()["Account"]
        account_aliases = iam_client.list_account_aliases()['AccountAliases']
        account_alias = account_aliases[0] if account_aliases else account_id

        # Define a list of users to ignore
        exclude_list = ['UserToExclude1', 'ServiceAccount', 'AutomationScript']

        # Extract event details
        event_detail = event.get('detail', {})
        event_name = event_detail.get('eventName')
        user_identity = event_detail.get('userIdentity', {}).get('userName', 'N/A')

        # Check if the event should be ignored
        if user_identity in exclude_list:
            logger.info(f"Event by user {user_identity} is excluded from notifications.")
            return {
                'statusCode': 200,
                'body': json.dumps(f"Event by user {user_identity} excluded.")
            }

        event_time = event_detail.get('eventTime')
        source_ip = event_detail.get('sourceIPAddress')
        userAgent = event_detail.get('userAgent')
        request_parameters = json.dumps(event_detail.get('requestParameters', {}), indent=4)
        error_message = event_detail.get('errorMessage', 'N/A')
        error_code = event_detail.get('errorCode', 'N/A')

        # Prepare the message
        message = (f"Event: {event_name}\nUser: {user_identity}\nTime: {event_time}\nIP: {source_ip}\n"
                   f"User Agent: {userAgent}\nRequest Parameters: {request_parameters}\n"
                   f"Error Message: {error_message}\nError Code: {error_code}")
        subject = f"IAM Activity Detected in {account_alias}"

        # Publish to SNS
        sns_response = sns_client.publish(
            TopicArn="arn:aws:sns:REGION:ACCOUNT_ID:SNS_TOPIC_NAME",  # Replace REGION, ACCOUNT_ID, and SNS_TOPIC_NAME
            Message=message,
            Subject=subject
        )

        logger.info(f"Successfully published to SNS: {sns_response}")

        return {
            'statusCode': 200,
            'body': json.dumps('Notification sent successfully')
        }

    except Exception as e:
        logger.error(f"Error processing the Lambda function: {str(e)}")
        raise Exception(f"Error processing the Lambda function: {str(e)}")