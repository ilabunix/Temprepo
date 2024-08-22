#!/bin/bash

# Usage: ./check_public_s3.sh <aws_profile>
PROFILE=$1

# Initialize counters
bucket_count=0
public_bucket_count=0

# Loop through all buckets and check their ACLs
for bucket in $(aws s3api list-buckets --query "Buckets[].Name" --profile $PROFILE --output text); do
    ((bucket_count++))
    result=$(aws s3api get-bucket-acl --bucket $bucket --profile $PROFILE --query "Grants[?Grantee.URI=='http://acs.amazonaws.com/groups/global/AllUsers' || Grantee.URI=='http://acs.amazonaws.com/groups/global/AuthenticatedUsers']" --output text)
    
    if [[ -n "$result" ]]; then
        ((public_bucket_count++))
    fi
done

# Final summary
echo "Total buckets scanned: $bucket_count"
echo "Publicly accessible buckets found: $public_bucket_count"