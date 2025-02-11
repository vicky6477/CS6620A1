import boto3
import json
import botocore.exceptions

# Initialize AWS clients
iam = boto3.client('iam')
sts = boto3.client('sts')

# Retrieve AWS Account ID
try:
    AWS_ACCOUNT_ID = sts.get_caller_identity()["Account"]
except botocore.exceptions.ClientError as e:
    print(f"Error retrieving AWS Account ID: {e}")
    exit(1)

IAM_USER_NAME = "vickyA1"  # The new IAM user

def user_exists(user_name):
    """Check if the IAM user already exists."""
    try:
        iam.get_user(UserName=user_name)
        return True
    except iam.exceptions.NoSuchEntityException:
        return False
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            return False
        raise  # Rethrow any other unexpected error

def create_user(user_name):
    """Create a new IAM user if it does not already exist."""
    if user_exists(user_name):
        print(f"IAM user {user_name} already exists.")
    else:
        print(f"Creating IAM user {user_name}...")
        try:
            iam.create_user(UserName=user_name)
            print(f"IAM user {user_name} created successfully.")
        except botocore.exceptions.ClientError as e:
            print(f"Failed to create IAM user: {e}")
            exit(1)

def attach_assume_role_policy(user_name):
    """Attach an inline policy to allow the IAM user to assume the Dev and User roles."""
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["iam:UpdateAssumeRolePolicy","sts:AssumeRole" ],
                "Resource": [
                    f"arn:aws:iam::{AWS_ACCOUNT_ID}:role/Dev",
                    f"arn:aws:iam::{AWS_ACCOUNT_ID}:role/User"
                ]
            }
        ]
    }

    try:
        iam.put_user_policy(
            UserName=user_name,
            PolicyName="AssumeRolesPolicy",
            PolicyDocument=json.dumps(policy_document)
        )
        print(f"AssumeRole policy attached to {user_name}.")
    except botocore.exceptions.ClientError as e:
        print(f"Failed to attach AssumeRole policy: {e}")
        exit(1)

# Create the IAM user
create_user(IAM_USER_NAME)

# Attach the AssumeRole policy to vickyA1
attach_assume_role_policy(IAM_USER_NAME)

print(f"User setup complete: {IAM_USER_NAME} can now assume Dev and User roles.")
