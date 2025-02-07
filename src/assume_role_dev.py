import boto3
from config import AWS_ACCOUNT_ID

sts = boto3.client('sts')

# Assume Dev role
assumed_role = sts.assume_role(
    RoleArn=f"arn:aws:iam::{AWS_ACCOUNT_ID}:role/Dev",
    RoleSessionName="DevSession"
)

credentials = assumed_role['Credentials']
s3 = boto3.client(
    's3',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)

# Create S3 bucket
bucket_name = f"vickya1bucket"
s3.create_bucket(Bucket=bucket_name)
print(f"S3 bucket {bucket_name} created successfully.")

# Store the bucket name in a file for later use
with open("bucket_name.txt", "w") as f:
    f.write(bucket_name)

# Upload text files
s3.put_object(Bucket=bucket_name, Key="assignment1.txt", Body="Empty Assignment 1")
print("assignment1.txt uploaded successfully.")

s3.put_object(Bucket=bucket_name, Key="assignment2.txt", Body="Empty Assignment 2")
print("assignment2.txt uploaded successfully.")



# Upload image
with open("data/recording1.jpg", "rb") as img:
    s3.put_object(Bucket=bucket_name, Key="recording1.jpg", Body=img)
    print(f"recording1.jpg uploaded successfully.")
