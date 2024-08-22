#!/bin/bash

# Usage: ./check_public_s3.sh <aws_profile>
PROFILE=$1

# List all buckets and check their ACLs
for bucket in $(aws s3api list-buckets --query "Buckets[].Name" --profile $PROFILE --output text); do
    echo "Checking bucket: $bucket"
    aws s3api get-bucket-acl --bucket $bucket --profile $PROFILE --query "Grants[?Grantee.URI=='http://acs.amazonaws.com/groups/global/AllUsers' || Grantee.URI=='http://acs.amazonaws.com/groups/global/AuthenticatedUsers']"
done