import boto3
import json
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_ACCOUNT_ID

iam = boto3.client('iam', 
                    aws_access_key_id=AWS_ACCESS_KEY_ID, 
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                    region_name=AWS_REGION)

def create_role(role_name, policy):
    try:
        # Create IAM role
        role = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps({
                'Version': '2012-10-17',
                'Statement': [{
                    'Effect': 'Allow',
                    'Principal': {'AWS': f'arn:aws:iam::{AWS_ACCOUNT_ID}:root'},
                    'Action': 'sts:AssumeRole'
                }]
            })
        )
        print(f"Role {role_name} created successfully.")

        # Attach policy to role
        iam.put_role_policy(
            RoleName=role_name,
            PolicyName=f"{role_name}Policy",
            PolicyDocument=json.dumps(policy)
        )
        print(f"Policy attached to role {role_name}.")
    except Exception as e:
        print(f"Failed to create role {role_name}: {e}")

# Dev role with full S3 access
dev_policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Effect': 'Allow',
        'Action': 's3:*',
        'Resource': '*'
    }]
}

# User role with read-only S3 access
user_policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Effect': 'Allow',
        'Action': ['s3:ListBucket', 's3:GetObject'],
        'Resource': '*'
    }]
}

# Create roles automatically
create_role("Dev", dev_policy)
create_role("User", user_policy)
