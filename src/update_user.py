import boto3
import json

iam = boto3.client('iam')

AWS_ACCOUNT_ID = boto3.client('sts').get_caller_identity()["Account"]
IAM_USER_NAME_OLD = "vicky"
IAM_USER_NAME_NEW = "vickyA1"

def update_trust_policy(role_name):
    """Update the trust policy of a given role to allow both vicky and vickyA1."""
    new_trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        f"arn:aws:iam::{AWS_ACCOUNT_ID}:user/{IAM_USER_NAME_OLD}",
                        f"arn:aws:iam::{AWS_ACCOUNT_ID}:user/{IAM_USER_NAME_NEW}"
                    ]
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    # Update the trust policy for the role
    iam.update_assume_role_policy(
        RoleName=role_name,
        PolicyDocument=json.dumps(new_trust_policy)
    )
    print(f"Updated trust policy for role {role_name}")

# Update both Dev and User roles
update_trust_policy("Dev")
update_trust_policy("User")

print("Trust policies updated successfully.")
