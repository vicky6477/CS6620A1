import boto3
from config import AWS_ACCOUNT_ID

sts = boto3.client('sts')

# Verify the current user
caller_identity = sts.get_caller_identity()
print(f"Current IAM User: {caller_identity['Arn']}")

# Assume User role
assumed_user_role = sts.assume_role(
    RoleArn=f"arn:aws:iam::{AWS_ACCOUNT_ID}:role/User",
    RoleSessionName="UserSession"
)

user_credentials = assumed_user_role['Credentials']
s3_user = boto3.client(
    's3',
    aws_access_key_id=user_credentials['AccessKeyId'],
    aws_secret_access_key=user_credentials['SecretAccessKey'],
    aws_session_token=user_credentials['SessionToken']
)

# Read the bucket name from the stored file
with open("bucket_name.txt", "r") as f:
    bucket_name = f.read().strip()

# Compute file size
response = s3_user.list_objects_v2(Bucket=bucket_name, Prefix="assignment")
total_size = sum(obj['Size'] for obj in response.get('Contents', []))
print(f"Total size of assignment files: {total_size} bytes.")

