import boto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

iam = boto3.client('iam', 
                    aws_access_key_id=AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                    region_name=AWS_REGION)

user_name = "VickyA1"

try:
    iam.create_user(UserName=user_name)
    print(f"IAM user {user_name} created successfully.")
except Exception as e:
    print(f"Failed to create user: {e}")
