import boto3
from config import AWS_ACCOUNT_ID

sts = boto3.client('sts')

# Verify the current user
caller_identity = sts.get_caller_identity()
print(f"Current IAM User: {caller_identity['Arn']}")

# Assume Dev role again
assumed_dev_role = sts.assume_role(
    RoleArn=f"arn:aws:iam::{AWS_ACCOUNT_ID}:role/Dev",
    RoleSessionName="DevSession"
)

dev_credentials = assumed_dev_role['Credentials']
s3_dev = boto3.client(
    's3',
    aws_access_key_id=dev_credentials['AccessKeyId'],
    aws_secret_access_key=dev_credentials['SecretAccessKey'],
    aws_session_token=dev_credentials['SessionToken']
)

# Read the bucket name from the stored file
with open("bucket_name.txt", "r") as f:
    bucket_name = f.read().strip()


# Delete all objects
response = s3_dev.list_objects_v2(Bucket=bucket_name)
if 'Contents' in response:
    for obj in response['Contents']:
        s3_dev.delete_object(Bucket=bucket_name, Key=obj['Key'])
        print(f"Deleted: {obj['Key']}.")

# Delete S3 bucket
s3_dev.delete_bucket(Bucket=bucket_name)
print(f"Bucket {bucket_name} deleted.")
