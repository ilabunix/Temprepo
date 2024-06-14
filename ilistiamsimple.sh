#!/bin/bash

# List all roles and filter those with AWS account in their trust policy
role_count=0
roles=$(aws iam list-roles --query 'Roles[*].RoleName' --output text)

for role in $roles; do
    trust_policy=$(aws iam get-role --role-name "$role" --query 'Role.AssumeRolePolicyDocument.Statement[*].Principal.AWS' --output text)
    if [[ $trust_policy == arn:aws:iam::* ]]; then
        echo "Role: $role"
        ((role_count++))
    fi
done

echo "Total roles with AWS account in their trust policy: $role_count"