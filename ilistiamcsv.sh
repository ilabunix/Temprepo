#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <AWS_PROFILE> <CSV_FILE>"
    exit 1
fi

# Get the arguments
AWS_PROFILE=$1
CSV_FILE=$2

# Initialize CSV file with headers
echo "RoleName,AWSAccount" > "$CSV_FILE"

# List all roles and filter those with AWS account in their trust policy
role_count=0
roles=$(aws iam list-roles --profile "$AWS_PROFILE" --query 'Roles[*].RoleName' --output text)

for role in $roles; do
    trust_policy=$(aws iam get-role --role-name "$role" --profile "$AWS_PROFILE" --query 'Role.AssumeRolePolicyDocument.Statement[*].Principal.AWS' --output text)
    if [[ $trust_policy == arn:aws:iam::* ]]; then
        # Extract AWS account number from ARN
        aws_account=$(echo "$trust_policy" | grep -oP 'arn:aws:iam::\K[0-9]+')
        echo "$role,$aws_account" >> "$CSV_FILE"
        ((role_count++))
    fi
done

echo "Total roles with AWS account in their trust policy: $role_count"
echo "Results saved to $CSV_FILE"