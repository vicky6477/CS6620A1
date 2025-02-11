import boto3
import json
import os

iam = boto3.client('iam')
sts = boto3.client('sts')

# Retrieve AWS Account ID dynamically
AWS_ACCOUNT_ID = sts.get_caller_identity()["Account"]

# Dev role Trust Policy
dev_trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
             "Principal": {
                "AWS": f"arn:aws:iam::{AWS_ACCOUNT_ID}:user/vicky"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

# create Dev role
iam.create_role(
    RoleName="Dev",
    AssumeRolePolicyDocument=json.dumps(dev_trust_policy)
)

# attach AmazonS3FullAccess policy to Dev role
iam.attach_role_policy(
    RoleName="Dev",
    PolicyArn="arn:aws:iam::aws:policy/AmazonS3FullAccess"
)

# User role Trust Policy    
user_trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
             "Principal": {
                "AWS": f"arn:aws:iam::{AWS_ACCOUNT_ID}:user/vicky"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

# create User role
iam.create_role(
    RoleName="User",
    AssumeRolePolicyDocument=json.dumps(user_trust_policy)
)

# User role only has read access to S3
user_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": "*"
        }
    ]
}

iam.put_role_policy(
    RoleName="User",
    PolicyName="UserS3ReadOnly",
    PolicyDocument=json.dumps(user_policy)
)

print("Dev and User IAM roles created successfully.")
